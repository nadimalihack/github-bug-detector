import pandas as pd
import numpy as np
import json
import joblib
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class ProductionNLPModelTrainer:
    def __init__(self):
        # We use a Pipeline to bundle the TF-IDF Vectorizer with the ML algorithm
        # This is a production best-practice for NLP
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))),
            ('clf', RandomForestClassifier(n_estimators=100, max_depth=20, n_jobs=-1, random_state=42))
        ])
        
    def load_and_merge_datasets(self):
        print("="*60)
        print("Loading Production Datasets...")
        print("="*60)
        
        texts = []
        labels = []
        
        # 1. Load github_issues.csv (2.85 GB)
        # We load a chunk of 50,000 rows to prevent Out-Of-Memory crashes while still having massive data
        csv_path = Path("dataset/github_issues.csv")
        if csv_path.exists():
            print(f"Loading {csv_path} (Reading first 50,000 rows to prevent OOM)...")
            try:
                # Use engine='python' or on_bad_lines='skip' to handle messy CSVs
                df_issues = pd.read_csv(csv_path, nrows=50000, on_bad_lines='skip')
                for _, row in df_issues.iterrows():
                    title = str(row.get('issue_title', ''))
                    body = str(row.get('body', ''))
                    text = f"{title} {body}"
                    if len(text.strip()) > 10:
                        texts.append(text)
                print(f" [SUCCESS] Extracted {len(df_issues)} issues from CSV.")
            except Exception as e:
                print(f" [ERROR] Error reading CSV: {e}")
        
        # 2. Load embold_test.json (19 MB)
        json_path = Path("dataset/embold_test.json")
        if json_path.exists():
            print(f"Loading {json_path}...")
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    for item in json_data:
                        title = item.get('title', '')
                        body = item.get('body', '')
                        text = f"{title} {body}"
                        if len(text.strip()) > 10:
                            texts.append(text)
                print(f" [SUCCESS] Extracted {len(json_data)} issues from JSON.")
            except Exception as e:
                print(f" [ERROR] Error reading JSON: {e}")
                
        # 3. Auto-Label the data (Semi-Supervised Approach)
        # Since the raw data doesn't have "Bug" vs "Feature" labels, we use heuristics for training.
        print("\nAuto-Labeling data using heuristic NLP detection...")
        bug_keywords = ['bug', 'error', 'fail', 'crash', 'exception', 'unexpected', 'issue', 'not working']
        
        for text in texts:
            text_lower = text.lower()
            # If any bug keyword is in the text, label as 1 (Bug). Else 0 (Feature/Enhancement)
            is_bug = 1 if any(kw in text_lower for kw in bug_keywords) else 0
            labels.append(is_bug)
            
        df = pd.DataFrame({
            'text': texts,
            'is_bug': labels
        })
        
        # Balance the dataset (downsample the majority class)
        bug_count = df['is_bug'].sum()
        clean_count = len(df) - bug_count
        min_count = min(bug_count, clean_count)
        
        if min_count > 0:
            df_bugs = df[df['is_bug'] == 1].sample(min_count, random_state=42)
            df_clean = df[df['is_bug'] == 0].sample(min_count, random_state=42)
            df = pd.concat([df_bugs, df_clean]).sample(frac=1, random_state=42).reset_index(drop=True)
            
        print(f"\nTotal balanced dataset size: {len(df)} samples.")
        print(f"Bugs: {df['is_bug'].sum()} | Enhancements/Questions: {len(df) - df['is_bug'].sum()}")
        return df

    def train(self, df):
        print("\n" + "="*60)
        print("Training Production NLP Pipeline (TF-IDF + Random Forest)...")
        print("="*60)
        
        X = df['text']
        y = df['is_bug']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit the pipeline
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate
        print("\nEvaluating Model on Test Set...")
        y_pred = self.pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"\n[SUCCESS] Test Accuracy: {acc:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Feature/Question', 'Bug/Error']))
        
        return acc

    def save_model(self, path="../models/issue_classifier.pkl"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)
        print(f"\n[SUCCESS] Production NLP Model saved successfully to {path}")

if __name__ == "__main__":
    trainer = ProductionNLPModelTrainer()
    df = trainer.load_and_merge_datasets()
    if len(df) > 10:
        trainer.train(df)
        trainer.save_model()
    else:
        print("Not enough data to train!")
