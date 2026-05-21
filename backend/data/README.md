# Training Data

This folder contains sample repository data for training the bug prediction model.

## Format

The `sample_repos.json` file should contain:

```json
{
  "repositories": [
    {
      "repository_name": "owner/repo",
      "commits": [
        {
          "hash": "commit_hash",
          "message": "commit message",
          "diff": "code changes",
          "files_changed": ["file1.js", "file2.js"]
        }
      ],
      "issues": [
        {
          "commit_hash": "commit_hash",
          "type": "bug|feature|enhancement|etc"
        }
      ]
    }
  ]
}
```

## Adding Your Own Data

1. Export commit history from your GitHub repository
2. Format it according to the schema above
3. Add it to `sample_repos.json`
4. Run `python trainer.py` to train the model

## Tips for Better Training

- Include at least 50+ commits for meaningful results
- Mix bug-related and non-bug commits
- Include diverse file types and modules
- Label issues accurately (bug vs feature)
