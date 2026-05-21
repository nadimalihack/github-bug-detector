"""Incremental Learning System - Learns from user feedback and past data"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from typing import Dict, List

class IncrementalLearner:
    """Self-learning model that improves from user feedback"""
    
    def __init__(self, model_path: str = "../models/bug_predictor.pkl",
                 data_path: str = "../data/learning_history.json"):
        self.model_path = Path(model_path)
        self.data_path = Path(data_path)
        self.model = None
        self.learning_history = []
        
        # Load existing model and history
        self.load_model()
        self.load_history()
        
    def load_model(self):
        """Load existing model or create new one"""
        try:
            self.model = joblib.load(self.model_path)
            print(f"[SUCCESS] Loaded existing model from {self.model_path}")
        except FileNotFoundError:
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                warm_start=True  # Enable incremental learning
            )
            print("[SUCCESS] Created new model for incremental learning")
    
    def load_history(self):
        """Load learning history from disk"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r') as f:
                    self.learning_history = json.load(f)
                print(f"[SUCCESS] Loaded {len(self.learning_history)} historical records")
        except Exception as e:
            print(f"[WARNING] Could not load history: {str(e)}")
            self.learning_history = []
    
    def save_history(self):
        """Save learning history to disk"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(self.learning_history, f, indent=2)
        print(f"[SUCCESS] Saved {len(self.learning_history)} records to history")
    
    def record_analysis(self, repo_data: Dict, prediction_result: Dict):
        """Record an analysis for future learning"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'repository': repo_data.get('repository_name'),
            'files_analyzed': len(prediction_result.get('modules', [])),
            'overall_risk': prediction_result.get('overall_repository_risk'),
            'modules': prediction_result.get('modules', []),
            'metadata': repo_data.get('metadata', {}),
            'feedback': None  # Will be updated when user provides feedback
        }
        
        self.learning_history.append(record)
        self.save_history()
        
        return len(self.learning_history) - 1  # Return record ID
    
    def add_user_feedback(self, record_id: int, file_name: str, 
                         actual_had_bugs: bool, severity: str = None):
        """Add user feedback about prediction accuracy"""
        if 0 <= record_id < len(self.learning_history):
            record = self.learning_history[record_id]
            
            if 'feedback' not in record or record['feedback'] is None:
                record['feedback'] = []
            
            feedback = {
                'file': file_name,
                'actual_had_bugs': actual_had_bugs,
                'severity': severity,
                'timestamp': datetime.now().isoformat()
            }
            
            record['feedback'].append(feedback)
            self.save_history()
            
            print(f"[SUCCESS] Recorded feedback for {file_name}")
            return True
        
        return False
    
    def prepare_training_data_from_history(self) -> pd.DataFrame:
        """Convert learning history into training data"""
        rows = []
        
        for record in self.learning_history:
            if not record.get('feedback'):
                continue  # Skip records without feedback
            
            # Create mapping of file -> actual bugs
            feedback_map = {
                f['file']: f['actual_had_bugs'] 
                for f in record['feedback']
            }
            
            # Process each module
            for module in record.get('modules', []):
                file_name = module['file']
                
                # Skip if no feedback for this file
                if file_name not in feedback_map:
                    continue
                
                rows.append({
                    'file': file_name,
                    'bug_keyword_count': module.get('code_quality_issues', 0),
                    'lines_changed': 50,  # Estimate
                    'commit_frequency': 1,  # Estimate
                    'predicted_risk': module['risk_score'],
                    'critical_issues': module.get('critical_issues', 0),
                    'high_issues': module.get('high_issues', 0),
                    'is_buggy': int(feedback_map[file_name])  # Actual label
                })
        
        return pd.DataFrame(rows)
    
    def retrain_model(self, min_feedback_samples: int = 10):
        """Retrain model with accumulated feedback"""
        df = self.prepare_training_data_from_history()
        
        if len(df) < min_feedback_samples:
            print(f"[WARNING] Not enough feedback samples ({len(df)}/{min_feedback_samples})")
            print("  Collect more user feedback before retraining")
            return False
        
        print(f"\n{'='*60}")
        print(f"Retraining Model with User Feedback")
        print(f"{'='*60}")
        print(f"Training samples: {len(df)}")
        print(f"Buggy files: {df['is_buggy'].sum()}")
        print(f"Clean files: {len(df) - df['is_buggy'].sum()}")
        
        # Prepare features
        feature_cols = ['bug_keyword_count', 'lines_changed', 'commit_frequency',
                       'critical_issues', 'high_issues']
        X = df[feature_cols]
        y = df['is_buggy']
        
        # Split for validation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = self.model.score(X_test, y_test)
        print(f"\n[SUCCESS] Model retrained with {accuracy:.2%} accuracy")
        
        # Save updated model
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"[SUCCESS] Updated model saved to {self.model_path}")
        
        return True
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learning progress"""
        total_records = len(self.learning_history)
        records_with_feedback = sum(
            1 for r in self.learning_history 
            if r.get('feedback')
        )
        
        total_feedback = sum(
            len(r.get('feedback', [])) 
            for r in self.learning_history
        )
        
        return {
            'total_analyses': total_records,
            'analyses_with_feedback': records_with_feedback,
            'total_feedback_items': total_feedback,
            'feedback_percentage': (records_with_feedback / total_records * 100) 
                                  if total_records > 0 else 0,
            'ready_for_retraining': total_feedback >= 10
        }
    
    def auto_retrain_if_ready(self, threshold: int = 20):
        """Automatically retrain if enough feedback collected"""
        stats = self.get_learning_stats()
        
        if stats['total_feedback_items'] >= threshold:
            print(f"\n[SUCCESS] Auto-retraining triggered ({stats['total_feedback_items']} feedback items)")
            return self.retrain_model()
        
        return False
