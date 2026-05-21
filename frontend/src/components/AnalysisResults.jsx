import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiAlertCircle, FiCheckCircle, FiCode, FiZap, FiMessageSquare, FiSend, FiLink } from 'react-icons/fi';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import './AnalysisResults.css';

const AnalysisResults = ({ result: initialResult, onClose }) => {
    const [result, setResult] = useState(initialResult);
    const [activeTab, setActiveTab] = useState('output');
    
    // Zustand Auth Integration to resolve Failed to Fetch / Authentication Issues
    const { token, user, githubToken } = useAuthStore();

    // Gemini Deep Audit States
    const [geminiLoading, setGeminiLoading] = useState(false);
    const [geminiError, setGeminiError] = useState(null);

    // Conversational RAG Chat States
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: `👋 Hello! I am your AI Codebase Companion. I have indexed the entire repository of **${result.repository_name}**. Ask me any specific questions about files, functions, vulnerabilities, or how to implement changes!`
        }
    ]);
    const [chatInput, setChatInput] = useState('');
    const [chatLoading, setChatLoading] = useState(false);
    const chatEndRef = useRef(null);

    // Auto scroll chat to bottom
    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, chatLoading]);

    const getRiskColor = (score) => {
        if (score >= 0.7) return '#da3633';
        if (score >= 0.4) return '#d29922';
        return '#238636';
    };

    const getRiskLevel = (score) => {
        if (score >= 0.7) return 'High';
        if (score >= 0.4) return 'Medium';
        return 'Low';
    };

    // Trigger Deep Gemini Analysis Instantly (Uses pre-computed ML summary under 2s!)
    const runGeminiAnalysis = async () => {
        setGeminiLoading(true);
        setGeminiError(null);
        try {
            console.log('🤖 Triggering instant Deep Gemini AI Audit via ML summary...');
            const res = await fetch(`${API_URL}/analyze/gemini/ml-summary`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                },
                body: JSON.stringify({
                    ml_data: {
                        repository: result.repository_name,
                        overall_risk: result.overall_repository_risk,
                        total_files: result.modules?.length || 0,
                        high_risk_files: result.modules?.filter(m => m.risk_score >= 0.7) || [],
                        modules: result.modules || [],
                        metadata: result.metadata || {}
                    },
                    user_id: user?.id || null
                })
            });

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || 'Failed to generate Deep AI Audit');
            }

            const geminiResult = await res.json();
            console.log('✅ Deep Gemini Audit Complete:', geminiResult);
            
            // Merge into active state
            setResult(prev => ({
                ...prev,
                gemini_analysis: geminiResult
            }));
        } catch (err) {
            console.error('❌ Gemini analysis failed:', err);
            setGeminiError(err.message || 'Gemini AI analysis failed. Please check key/quota.');
        } finally {
            setGeminiLoading(false);
        }
    };

    // Send Message to Conversational RAG Chat Endpoint
    const sendChatMessage = async (e) => {
        if (e) e.preventDefault();
        if (!chatInput.trim() || chatLoading) return;

        const userMsg = chatInput.trim();
        setChatInput('');
        
        // Append user query to thread
        const updatedMsgs = [...messages, { role: 'user', content: userMsg }];
        setMessages(updatedMsgs);
        setChatLoading(true);

        try {
            console.log('💬 Submitting conversational RAG query...');
            const res = await fetch(`${API_URL}/analyze-chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                },
                body: JSON.stringify({
                    repo_url: result.repository_name,
                    question: userMsg,
                    session_id: `session_${result.repository_name.replace(/\//g, '_')}`,
                    access_token: githubToken || null,
                    user_id: user?.id || null,
                    history: updatedMsgs // Pass conversation thread history!
                })
            });

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || 'Chat request failed');
            }

            const data = await res.json();
            console.log('✅ RAG Answer received:', data);

            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: data.answer,
                    sources: data.sources || []
                }
            ]);
        } catch (err) {
            console.error('❌ RAG Chat failed:', err);
            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: `⚠️ Sorry, I encountered an error while processing that query: ${err.message}. Please make sure the backend is active.`
                }
            ]);
        } finally {
            setChatLoading(false);
        }
    };

    return (
        <motion.div
            className="analysis-results-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
        >
            <motion.div
                className="analysis-results-modal"
                initial={{ scale: 0.95, y: 20 }}
                animate={{ scale: 1, y: 0 }}
                exit={{ scale: 0.95, y: 20 }}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="modal-header">
                    <h2>{result.repository_name}</h2>
                    <button onClick={onClose} className="close-btn">×</button>
                </div>

                <div className="tabs">
                    <button
                        className={activeTab === 'output' ? 'tab active' : 'tab'}
                        onClick={() => setActiveTab('output')}
                    >
                        <FiCode /> Output
                    </button>
                    <button
                        className={activeTab === 'gemini' ? 'tab active' : 'tab'}
                        onClick={() => setActiveTab('gemini')}
                    >
                        <FiZap /> Gemini Analysis
                    </button>
                    <button
                        className={activeTab === 'chat' ? 'tab active' : 'tab'}
                        onClick={() => setActiveTab('chat')}
                    >
                        <FiMessageSquare /> Codebase Chat
                    </button>
                </div>

                <div className="tab-content">
                    {/* Output Tab - Traditional ML & Overview stats */}
                    {activeTab === 'output' && (
                        <div className="output-tab">
                            <div className="overall-risk">
                                <h3>Overall Repository Risk</h3>
                                <div
                                    className="risk-score"
                                    style={{ color: getRiskColor(result.overall_repository_risk) }}
                                >
                                    {(result.overall_repository_risk * 100).toFixed(0)}%
                                    <span className="risk-level">
                                        {getRiskLevel(result.overall_repository_risk)}
                                    </span>
                                </div>
                            </div>

                            {/* Lines Summary Stats - Prevents "75 Readme" Label Confusion */}
                            {result.metadata && (
                                <div className="metadata">
                                    <span>⭐ {result.metadata.stars || 0} Stars</span>
                                    <span>🔱 {result.metadata.forks || 0} Forks</span>
                                    <span>🔤 {result.metadata.language || 'N/A'}</span>
                                    {result.metadata.loc && (
                                        <>
                                            <span style={{ color: '#58a6ff' }}>📝 {result.metadata.loc.total_loc || 0} Total Lines</span>
                                            <span style={{ color: '#3fb950' }}>🧪 {result.metadata.loc.test_loc || 0} Test Lines</span>
                                            <span style={{ color: '#d29922' }}>📖 {result.metadata.loc.readme_loc || 0} Readme Lines</span>
                                            <span style={{ color: '#bc8cff' }}>📦 {result.metadata.loc.artifact_loc || 0} Artifact Lines</span>
                                        </>
                                    )}
                                </div>
                            )}

                            <div className="modules-list">
                                <h3>Risky Files ({result.modules?.length || 0})</h3>
                                {result.modules?.map((module, index) => (
                                    <div key={index} className="module-card">
                                        <div className="module-header">
                                            <span className="file-name">{module.file}</span>
                                            <span
                                                className="module-risk"
                                                style={{ color: getRiskColor(module.risk_score) }}
                                            >
                                                {(module.risk_score * 100).toFixed(0)}%
                                            </span>
                                        </div>
                                        <p className="module-reason">{module.reason}</p>

                                        {module.code_issues && module.code_issues.length > 0 && (
                                            <div className="code-issues">
                                                <h4>
                                                    <FiAlertCircle /> Code Issues ({module.code_issues[0].issues})
                                                </h4>
                                                {module.code_issues[0].detailed_issues?.map((issue, idx) => (
                                                    <div key={idx} className={`issue-item severity-${issue.severity}`}>
                                                        <div className="issue-header">
                                                            <span className="issue-type">{issue.type}</span>
                                                            <span className="issue-severity">{issue.severity}</span>
                                                        </div>
                                                        <p className="issue-message">{issue.message}</p>
                                                        {issue.code_snippet && (
                                                            <code className="code-snippet">{issue.code_snippet}</code>
                                                        )}
                                                        <p className="issue-fix">
                                                            <FiCheckCircle /> {issue.fix}
                                                        </p>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Gemini Analysis Tab */}
                    {activeTab === 'gemini' && (
                        <div className="gemini-tab">
                            {result.gemini_analysis ? (
                                <div className="gemini-overview">
                                    <h3>🤖 AI Deep Security Audit</h3>
                                    <div className="gemini-risk" style={{ fontSize: '1.2rem', fontWeight: 'bold', margin: '1rem 0' }}>
                                        Overall AI Assessment: <span style={{ color: getRiskColor(result.gemini_analysis.overall_risk / 100) }}>{result.gemini_analysis.overall_risk || 0}%</span>
                                    </div>
                                    <p style={{ color: '#8b949e' }}>Files Evaluated: {result.gemini_analysis.files_analyzed || 0}</p>

                                    {result.gemini_analysis.summary && (
                                        <div className="gemini-summary" style={{ background: '#161b22', padding: '1.25rem', borderRadius: '6px', margin: '1.5rem 0', border: '1px solid #30363d' }}>
                                            <h4 style={{ margin: '0 0 0.5rem 0', color: '#c9d1d9' }}>Executive Summary</h4>
                                            <p style={{ margin: 0, lineHeight: 1.6, color: '#8b949e' }}>{result.gemini_analysis.summary}</p>
                                        </div>
                                    )}

                                    {result.gemini_analysis.critical_concerns && result.gemini_analysis.critical_concerns.length > 0 && (
                                        <div className="gemini-section" style={{ margin: '1.5rem 0' }}>
                                            <h4 style={{ color: '#ff7b72' }}>⚠️ Critical Vulnerabilities & Concerns</h4>
                                            <ul style={{ paddingLeft: '1.25rem', color: '#c9d1d9', lineHeight: 1.7 }}>
                                                {result.gemini_analysis.critical_concerns.map((concern, i) => (
                                                    <li key={i} style={{ marginBottom: '0.5rem' }}>
                                                        {typeof concern === 'string' ? concern : (
                                                            <>
                                                                {concern.issue && <strong>{concern.issue}: </strong>}
                                                                {concern.description || concern.title || JSON.stringify(concern)}
                                                            </>
                                                        )}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {result.gemini_analysis.recommendations && result.gemini_analysis.recommendations.length > 0 && (
                                        <div className="gemini-section" style={{ margin: '1.5rem 0' }}>
                                            <h4 style={{ color: '#58a6ff' }}>💡 Actionable Fixes & Improvement Strategy</h4>
                                            <ul style={{ paddingLeft: '1.25rem', color: '#c9d1d9', lineHeight: 1.7 }}>
                                                {result.gemini_analysis.recommendations.map((rec, i) => (
                                                    <li key={i} style={{ marginBottom: '0.5rem' }}>
                                                        {typeof rec === 'string' ? rec : (
                                                            <>
                                                                {rec.title && <strong>{rec.title}: </strong>}
                                                                {rec.description || rec.details || JSON.stringify(rec)}
                                                            </>
                                                        )}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {result.gemini_analysis.files && result.gemini_analysis.files.length > 0 && (
                                        <div className="gemini-files-list" style={{ marginTop: '2rem' }}>
                                            <h4 style={{ color: '#c9d1d9', borderBottom: '1px solid #30363d', paddingBottom: '0.5rem' }}>File-by-File AI Solutions</h4>
                                            {result.gemini_analysis.files.map((file, index) => (
                                                <div key={index} className="gemini-file" style={{ background: '#161b22', border: '1px solid #30363d', borderRadius: '6px', padding: '1.25rem', margin: '1rem 0' }}>
                                                    <h5 style={{ margin: '0 0 0.5rem 0', color: '#58a6ff', fontSize: '1rem' }}>{file.filename}</h5>
                                                    <div style={{ fontSize: '0.875rem', color: getRiskColor(file.risk_score/100), fontWeight: 'bold', marginBottom: '1rem' }}>
                                                        Risk: {file.risk_score}%
                                                    </div>

                                                    {file.vulnerabilities?.length > 0 && (
                                                        <div style={{ marginBottom: '0.75rem' }}>
                                                            <strong style={{ color: '#ff7b72', fontSize: '0.85rem' }}>🔒 Vulnerabilities:</strong>
                                                            <ul style={{ margin: '0.25rem 0', paddingLeft: '1.25rem', fontSize: '0.875rem', color: '#c9d1d9' }}>
                                                                {file.vulnerabilities.map((v, i) => <li key={i}>{typeof v === 'string' ? v : JSON.stringify(v)}</li>)}
                                                            </ul>
                                                        </div>
                                                    )}

                                                    {file.suggestions?.length > 0 && (
                                                        <div>
                                                            <strong style={{ color: '#58a6ff', fontSize: '0.85rem' }}>💡 Recommendations:</strong>
                                                            <ul style={{ margin: '0.25rem 0', paddingLeft: '1.25rem', fontSize: '0.875rem', color: '#c9d1d9' }}>
                                                                {file.suggestions.map((s, i) => <li key={i}>{typeof s === 'string' ? s : JSON.stringify(s)}</li>)}
                                                            </ul>
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ) : (
                                /* Glassmorphic Call-to-Action to Trigger Deep AI Audit */
                                <div className="trigger-card">
                                    <h3 className="trigger-title">🤖 Deep AI Security Audit Not Yet Run</h3>
                                    <p className="trigger-desc">
                                        Activate Gemini 2.5 Flash to execute an advanced threat detection audit across this codebase. Get a detailed executive summary, security posture breakdown, and precise codebase suggestions instantly.
                                    </p>
                                    
                                    {geminiError && (
                                        <div style={{ color: '#ff7b72', margin: '1rem 0', fontSize: '0.9rem' }}>
                                            ⚠️ {geminiError}
                                        </div>
                                    )}

                                    <button
                                        onClick={runGeminiAnalysis}
                                        disabled={geminiLoading}
                                        className="trigger-btn"
                                    >
                                        {geminiLoading ? (
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                                <div className="loading-spinner" style={{ width: '18px', height: '18px', borderSize: '2px' }}></div>
                                                Running Deep AI Audit...
                                            </div>
                                        ) : (
                                            'Run Deep Gemini Analysis'
                                        )}
                                    </button>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Conversational RAG Codebase Chat Tab */}
                    {activeTab === 'chat' && (
                        <div className="chat-tab">
                            <div className="chat-history">
                                {messages.map((msg, index) => (
                                    <div key={index} className={`chat-message ${msg.role}`}>
                                        <div style={{ whiteSpace: 'pre-wrap' }}>
                                            {msg.content}
                                        </div>
                                        
                                        {/* Display code sources referenced by the RAG index */}
                                        {msg.sources && msg.sources.length > 0 && (
                                            <div className="chat-message-sources">
                                                <div className="sources-title">
                                                    <FiLink style={{ marginRight: '4px' }} /> Referenced Code Snippets:
                                                </div>
                                                <div className="sources-grid">
                                                    {msg.sources.map((source, sIdx) => (
                                                        <div
                                                            key={sIdx}
                                                            className="source-card"
                                                            title={source.content}
                                                            onClick={() => alert(`--- File: ${source.file} ---\n\n${source.content}`)}
                                                        >
                                                            {source.file.split('/').pop()}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                                
                                {chatLoading && (
                                    <div className="typing-indicator">
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                    </div>
                                )}
                                
                                <div ref={chatEndRef} />
                            </div>

                            <form onSubmit={sendChatMessage} className="chat-input-container">
                                <input
                                    type="text"
                                    value={chatInput}
                                    onChange={(e) => setChatInput(e.target.value)}
                                    placeholder={`Ask a question about ${result.repository_name}...`}
                                    className="chat-input"
                                    disabled={chatLoading}
                                />
                                <button
                                    type="submit"
                                    className="chat-send-btn"
                                    disabled={chatLoading || !chatInput.trim()}
                                >
                                    <FiSend /> Send
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            </motion.div>
        </motion.div>
    );
};

export default AnalysisResults;
