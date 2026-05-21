"""
Retrieval-Augmented Generation (RAG) engine for GitHub Repositories
Allows users to ask questions about a repository's codebase.
"""

import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

from .repo_evaluator_engine import clone_repo, detect_platform, parse_repo_name

logger = logging.getLogger(__name__)

class RepoRAG:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the RAG engine with Gemini."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for RAG")
            
        # Initialize Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=self.api_key
        )
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash", 
            google_api_key=self.api_key,
            temperature=0.2
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # The Vector Store instance
        self.vector_store = None
        self.repo_url = None
        self.repo_dir = None
        
    def _is_code_file(self, filepath: str) -> bool:
        """Filter out binaries and non-text files."""
        # Simple extension check or skip hidden dirs
        path_obj = Path(filepath)
        if any(part.startswith('.') for part in path_obj.parts):
            return False
            
        EXTENSIONS_TO_INDEX = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.html', '.css', 
            '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb', '.php', '.md', '.txt'
        }
        return path_obj.suffix.lower() in EXTENSIONS_TO_INDEX

    def load_and_index_repo(self, repo_url: str, token: Optional[str] = None) -> bool:
        """Clone and index a GitHub repository for RAG."""
        self.repo_url = repo_url
        self.repo_dir = Path(tempfile.mkdtemp(prefix='rag_repo_'))
        
        try:
            # 1. Detect Platform
            platform = detect_platform(repo_url)
            
            # 2. Parse Repo Name
            owner, repo_name = parse_repo_name(repo_url)
            logger.info(f"RAG: Cloning {owner}/{repo_name}...")
            
            # 3. Clone Repository (shallow = only latest snapshot, much faster for RAG)
            repo_path = clone_repo(
                f"{owner}/{repo_name}",
                self.repo_dir,
                token or "",
                platform,
                shallow=True,
            )
            
            # 4. Read files and chunk
            documents = []
            logger.info("RAG: Reading files...")
            for root, _, files in os.walk(repo_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self._is_code_file(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Create a document
                            rel_path = os.path.relpath(file_path, repo_path)
                            documents.append(Document(
                                page_content=content,
                                metadata={"source": rel_path}
                            ))
                        except Exception as e:
                            logger.debug(f"Skipping {file_path}: {e}")
                            
            if not documents:
                raise ValueError("No readable code files found in repository")
                
            # 5. Split chunks
            logger.info(f"RAG: Splitting {len(documents)} files into chunks...")
            chunks = self.text_splitter.split_documents(documents)
            
            # 6. Build index (cap at 2000 chunks for speed/cost if needed)
            logger.info(f"RAG: Building FAISS index for {len(chunks)} chunks...")
            if len(chunks) > 2000:
                logger.warning("RAG: Too many chunks, limiting to 2000 for safety.")
                chunks = chunks[:2000]
                
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            logger.info("RAG: Index build complete!")
            return True
            
        except Exception as e:
            logger.error(f"RAG Indexing failed: {e}")
            self.cleanup()
            raise
            
    def query(self, question: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Ask a question to the codebase with conversation context."""
        if not self.vector_store:
            raise ValueError("Repository not indexed. Call load_and_index_repo first.")
            
        search_query = question
        formatted_history = ""
        
        if history:
            history_blocks = []
            for msg in history[-6:]: # Get last 6 messages
                role_label = "User" if msg.get("role") == "user" else "Assistant"
                history_blocks.append(f"{role_label}: {msg.get('content')}")
            formatted_history = "\n".join(history_blocks)
            
            # Reformulate query to contain full conversational context for vector lookup
            reformulation_prompt = f"""Given the following conversation history and a follow-up question, rephrase the follow-up question to be a standalone query that contains all necessary context for a vector search engine to locate relevant code snippets in a repository. Do NOT answer the question, just return the rephrased standalone query.

Conversation History:
{formatted_history}

Follow-up Question: {question}

Standalone Query:"""
            try:
                reformulation_response = self.llm.invoke(reformulation_prompt)
                rephrased = reformulation_response.content.strip()
                if rephrased:
                    search_query = rephrased
                    logger.info(f"RAG: Reformulated '{question}' -> '{search_query}'")
            except Exception as e:
                logger.warning(f"RAG: Query reformulation failed: {e}")

        # Retrieve top 5 most relevant code chunks based on the contextualized search query
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(search_query)
        
        # Build context prompt
        context = "\n\n".join([f"--- File: {doc.metadata.get('source', 'Unknown')} ---\n{doc.page_content}" for doc in docs])
        
        prompt = f"""You are an elite Software Engineer analyzing a codebase via Retrieval-Augmented Generation (RAG).
Answer the user's question insightfully based on the provided codebase snippets and conversation history.
Always write clean, professional, production-ready explanations with precise file references.

Conversation History:
{formatted_history if formatted_history else "No previous conversation."}

Codebase Snippets (Relevant to '{search_query}'):
{context}

Question: {question}

Provide a detailed, professional answer with complete markdown formatting. Highlight precise file names (e.g. `src/store/authStore.js`) and class/function names. Keep your answers comprehensive, detailed, and directly action-oriented."""

        # Call Gemini
        response = self.llm.invoke(prompt)
        
        return {
            "answer": response.content,
            "sources": [{"file": doc.metadata.get('source'), "content": doc.page_content[:200] + "..."} for doc in docs]
        }
        
    def cleanup(self):
        """Remove temp directory."""
        if self.repo_dir and Path(self.repo_dir).exists():
            shutil.rmtree(str(self.repo_dir), ignore_errors=True)
            self.repo_dir = None
