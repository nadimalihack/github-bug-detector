"""Train model using real GitHub repositories"""
import sys
sys.path.append('src')

from github_analyzer import GitHubAnalyzer
from trainer import BugPredictionTrainer
import json
from pathlib import Path

# List of repositories to train on
TRAINING_REPOS = [
    "octocat/Hello-World",
    "torvalds/linux",
    "facebook/react",
    "microsoft/vscode",
    "nodejs/node"
]

def collect_training_data(repos, token=None, max_commits=50):
    """Collect training data from multiple GitHub repositories"""
    print("=" * 70)
    print("Collecting Training Data from GitHub")
    print("=" * 70)
    
    analyzer = GitHubAnalyzer(access_token=token)
    all_repos_data = []
    
    for repo_url in repos:
        try:
            print(f"\n📦 Analyzing: {repo_url}")
            repo_data = analyzer.analyze_repository(repo_url, max_commits=max_commits)
            all_repos_data.append(repo_data)
            print(f"✓ Collected {len(repo_data['commits'])} commits")
        except Exception as e:
            print(f"✗ Failed to analyze {repo_url}: {str(e)}")
            continue
    
    # Save collected data
    output_file = Path(__file__).parent / "data" / "github_training_data.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({"repositories": all_repos_data}, f, indent=2)
    
    print(f"\n✓ Saved training data to: {output_file}")
    return all_repos_data

def train_model_from_data(repos_data):
    """Train the ML model from collected data"""
    print("\n" + "=" * 70)
    print("Training ML Model")
    print("=" * 70)
    
    trainer = BugPredictionTrainer()
    
    # Prepare training data from all repos
    all_data = []
    for repo_data in repos_data:
        print(f"\nProcessing: {repo_data['repository_name']}")
        df = trainer.prepare_training_data(repo_data)
        all_data.append(df)
        print(f"  Files: {len(df)}, Buggy: {df['is_buggy'].sum()}")
    
    # Combine all data
    import pandas as pd
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("\n" + "=" * 70)
    print(f"Total samples: {len(combined_df)}")
    print(f"Buggy files: {combined_df['is_buggy'].sum()}")
    print(f"Clean files: {len(combined_df) - combined_df['is_buggy'].sum()}")
    print("=" * 70)
    
    if len(combined_df) < 10:
        print("\n⚠ Warning: Not enough data for good training")
        print("Consider adding more repositories or increasing max_commits")
    
    # Train
    accuracy = trainer.train(combined_df)
    
    # Save model
    trainer.save_model()
    
    print(f"\n✓ Model trained with {accuracy:.2%} accuracy")
    print("✓ Model saved to: ../models/bug_predictor.pkl")
    
    return accuracy

if __name__ == "__main__":
    import os
    
    # Get token from environment or prompt
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("\n⚠ No GitHub token found!")
        print("Set GITHUB_TOKEN environment variable or create backend/.env file")
        print("\nYou can still train with limited data (60 requests/hour)")
        response = input("\nContinue without token? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Get a token at: https://github.com/settings/tokens")
            exit(1)
    
    # Collect data
    print("\nCollecting data from GitHub repositories...")
    repos_data = collect_training_data(TRAINING_REPOS, token=token, max_commits=30)
    
    if not repos_data:
        print("\n✗ No data collected. Cannot train model.")
        exit(1)
    
    # Train model
    train_model_from_data(repos_data)
    
    print("\n" + "=" * 70)
    print("🎉 Training Complete!")
    print("=" * 70)
    print("\nRestart the API server to use the new model:")
    print("  cd backend/src")
    print("  python api.py")
