import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
from pathlib import Path
from .utils import extract_features, BUG_KEYWORDS

class BugPredictionTrainer:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = ['bug_keyword_count', 'lines_changed', 'commit_frequency']
        
    def prepare_training_data(self, repo_data: dict) -> pd.DataFrame:
        """Convert repository data into training dataset"""
        rows = []
        
        commits = repo_data.get('commits', [])
        issues = {issue['commit_hash']: issue['type'] for issue in repo_data.get('issues', [])}
        
        # Aggregate by file
        file_stats = {}
        for commit in commits:
            for file in commit.get('files_changed', []):
                if file not in file_stats:
                    file_stats[file] = {'commits': [], 'bug_count': 0}
                
                file_stats[file]['commits'].append(commit)
                
                # Check if this commit is bug-related
                commit_hash = commit.get('hash', '')
                is_bug = issues.get(commit_hash) == 'bug' or any(
                    kw in commit.get('message', '').lower() for kw in BUG_KEYWORDS
                )
                if is_bug:
                    file_stats[file]['bug_count'] += 1
        
        # Create features
        for file, stats in file_stats.items():
            total_commits = len(stats['commits'])
            bug_commits = stats['bug_count']
            avg_lines = np.mean([len(c.get('diff', '').split('\n')) for c in stats['commits']])
            
            rows.append({
                'file': file,
                'bug_keyword_count': bug_commits,
                'lines_changed': avg_lines,
                'commit_frequency': total_commits,
                'is_buggy': int(bug_commits / total_commits > 0.3) if total_commits > 0 else 0
            })
        
        return pd.DataFrame(rows)
    
    def train(self, training_data: pd.DataFrame):
        """Train the bug prediction model"""
        X = training_data[self.feature_columns]
        y = training_data['is_buggy']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return accuracy
    
    def save_model(self, path: str = "../models/bug_predictor.pkl"):
        """Save trained model"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")
    
    def load_model(self, path: str = "../models/bug_predictor.pkl"):
        """Load trained model"""
        self.model = joblib.load(path)
        print(f"Model loaded from {path}")

if __name__ == "__main__":
    print("=" * 60)
    print("Bug Prediction Model Trainer")
    print("=" * 60)
    
    # Load training data
    data_path = Path(__file__).parent.parent / "data" / "sample_repos.json"
    
    if not data_path.exists():
        print(f"\nError: Training data not found at {data_path}")
        print("Please ensure sample_repos.json exists in the data/ folder")
        exit(1)
    
    print(f"\nLoading data from: {data_path}")
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    trainer = BugPredictionTrainer()
    
    # Combine all repositories into one training dataset
    all_data = []
    for repo in data.get('repositories', []):
        print(f"\nProcessing repository: {repo['repository_name']}")
        df = trainer.prepare_training_data(repo)
        all_data.append(df)
        print(f"  - Files analyzed: {len(df)}")
        print(f"  - Buggy files: {df['is_buggy'].sum()}")
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("\n" + "=" * 60)
    print(f"Total training samples: {len(combined_df)}")
    print(f"Buggy files: {combined_df['is_buggy'].sum()}")
    print(f"Clean files: {len(combined_df) - combined_df['is_buggy'].sum()}")
    print("=" * 60)
    
    print("\nSample of training data:")
    print(combined_df.head(10))
    
    # Train the model
    print("\n" + "=" * 60)
    print("Training model...")
    print("=" * 60)
    
    if len(combined_df) < 5:
        print("\nWarning: Not enough data for proper training.")
        print("The model will be trained but may not be accurate.")
        print("Consider adding more repository data to sample_repos.json")
    
    accuracy = trainer.train(combined_df)
    
    # Save the model
    print("\n" + "=" * 60)
    trainer.save_model()
    print("=" * 60)
    
    print("\n✓ Training complete!")
    print(f"✓ Model accuracy: {accuracy:.2%}")
    print("✓ Model saved to: ../models/bug_predictor.pkl")
    print("\nYou can now use this model in the API by restarting the server.")
