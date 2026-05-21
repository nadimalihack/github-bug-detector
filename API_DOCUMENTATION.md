# API Documentation

Complete API reference for the GitHub Bug Detection System.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com/api
```

## Authentication

Most endpoints require authentication via JWT tokens obtained through GitHub OAuth.

### Headers

```http
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Endpoints

### Health Check

#### GET /

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GitHub URL Analysis

#### POST /analyze-github-url

Analyze a GitHub repository by URL.

**Request Body:**
```json
{
  "github_url": "facebook/react",
  "github_token": "ghp_optional_token",
  "max_commits": 100,
  "include_code_analysis": true
}
```

**Parameters:**
- `github_url` (required): GitHub repository URL or owner/repo format
- `github_token` (optional): GitHub personal access token for higher rate limits
- `max_commits` (optional): Maximum number of commits to analyze (default: 100)
- `include_code_analysis` (optional): Include detailed code analysis (default: false)

**Response:**
```json
{
  "repository_name": "facebook/react",
  "overall_repository_risk": 0.65,
  "total_files_analyzed": 150,
  "high_risk_files": 12,
  "analysis_timestamp": "2024-01-15T10:30:00Z",
  "modules": [
    {
      "file": "src/auth/AuthController.js",
      "risk_score": 0.85,
      "reason": "High frequency of bug-related commits and complex authentication logic",
      "recommendations": [
        "Add comprehensive unit tests",
        "Implement input validation",
        "Add rate limiting"
      ],
      "commit_count": 45,
      "bug_keywords": 12,
      "last_modified": "2024-01-10T15:20:00Z"
    }
  ],
  "statistics": {
    "total_commits": 1250,
    "bug_related_commits": 180,
    "average_risk_score": 0.42,
    "files_by_risk": {
      "high": 12,
      "medium": 45,
      "low": 93
    }
  }
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid repository URL
- `401 Unauthorized`: Invalid GitHub token
- `404 Not Found`: Repository not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

### File Upload Analysis

#### POST /analyze-github-file

Analyze repository data from uploaded JSON file.

**Request:**
- Content-Type: `multipart/form-data`
- File field name: `file`

**File Format:**
```json
{
  "commits": [
    {
      "sha": "abc123",
      "message": "fix: critical bug",
      "author": "developer",
      "date": "2024-01-15T10:30:00Z",
      "files": [
        {
          "filename": "auth.py",
          "additions": 10,
          "deletions": 5,
          "changes": 15
        }
      ]
    }
  ]
}
```

**Response:**
Same format as `/analyze-github-url`

---

### Prediction

#### POST /predict

Predict bug risk from commit data.

**Request Body:**
```json
{
  "commits": [
    {
      "sha": "abc123",
      "message": "fix: authentication bug",
      "files": [
        {
          "filename": "auth.py",
          "additions": 10,
          "deletions": 5
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "repository_name": "unknown",
  "overall_repository_risk": 0.72,
  "modules": [
    {
      "file": "auth.py",
      "risk_score": 0.82,
      "reason": "Frequent bug-related commits detected"
    }
  ]
}
```

---

### Code Analysis

#### POST /analyze-code

Analyze code snippet for vulnerabilities and code smells.

**Request Body:**
```json
{
  "code": "def authenticate(username, password):\n    query = f\"SELECT * FROM users WHERE username='{username}'\"",
  "language": "python",
  "context": "Authentication module"
}
```

**Response:**
```json
{
  "issues": [
    {
      "type": "SQL Injection",
      "severity": "critical",
      "line": 2,
      "description": "Potential SQL injection vulnerability",
      "recommendation": "Use parameterized queries instead of string formatting",
      "code_snippet": "query = f\"SELECT * FROM users WHERE username='{username}'\""
    }
  ],
  "complexity_score": 0.65,
  "total_issues": 1,
  "critical_issues": 1,
  "high_issues": 0,
  "medium_issues": 0,
  "low_issues": 0
}
```

---

### Authentication

#### GET /auth/github/login

Initiate GitHub OAuth flow.

**Response:**
Redirects to GitHub OAuth authorization page.

---

#### GET /auth/github/callback

GitHub OAuth callback endpoint.

**Query Parameters:**
- `code`: Authorization code from GitHub
- `state`: State parameter for CSRF protection

**Response:**
Redirects to frontend with JWT token.

---

#### GET /auth/user

Get authenticated user profile.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "id": "12345",
  "username": "developer",
  "email": "dev@example.com",
  "avatar_url": "https://avatars.githubusercontent.com/u/12345",
  "github_token": "ghp_encrypted_token"
}
```

---

#### POST /auth/logout

Logout user and invalidate token.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

---

### User Statistics

#### GET /api/user/stats

Get user's analysis statistics.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "total_analyses": 45,
  "repositories_analyzed": 12,
  "total_files_analyzed": 1250,
  "high_risk_files_found": 85,
  "average_risk_score": 0.52,
  "analyses_by_date": [
    {
      "date": "2024-01-15",
      "count": 5
    }
  ],
  "top_repositories": [
    {
      "name": "user/repo",
      "analyses": 8,
      "avg_risk": 0.65
    }
  ]
}
```

---

#### GET /api/user/repositories

Get user's analyzed repositories.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `sort` (optional): Sort field (default: "last_analyzed")
- `order` (optional): Sort order "asc" or "desc" (default: "desc")

**Response:**
```json
{
  "repositories": [
    {
      "name": "facebook/react",
      "last_analyzed": "2024-01-15T10:30:00Z",
      "overall_risk": 0.65,
      "total_files": 150,
      "high_risk_files": 12
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 12,
    "pages": 2
  }
}
```

---

### Feedback and Learning

#### POST /api/feedback

Submit feedback for model improvement.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "file": "auth.py",
  "repository": "user/repo",
  "predicted_risk": 0.85,
  "actual_has_bug": true,
  "bug_type": "SQL Injection",
  "severity": "critical",
  "comments": "Found SQL injection vulnerability"
}
```

**Response:**
```json
{
  "message": "Feedback submitted successfully",
  "feedback_id": "fb_12345",
  "training_queued": true
}
```

---

#### GET /api/training/progress

Get model training progress.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "status": "training",
  "progress": 65,
  "current_epoch": 13,
  "total_epochs": 20,
  "accuracy": 0.87,
  "loss": 0.23,
  "estimated_completion": "2024-01-15T11:00:00Z"
}
```

---

### Gemini AI Analysis

#### POST /api/gemini/analyze

Analyze code using Gemini AI.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "code": "function authenticate(user, pass) { ... }",
  "context": "User authentication",
  "analysis_type": "security"
}
```

**Response:**
```json
{
  "analysis": "The code has potential security vulnerabilities...",
  "recommendations": [
    "Implement password hashing",
    "Add rate limiting",
    "Use secure session management"
  ],
  "severity": "high",
  "confidence": 0.92
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

- `INVALID_REQUEST`: Request validation failed
- `UNAUTHORIZED`: Authentication required or failed
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## Rate Limiting

API requests are rate-limited to prevent abuse:

- **Without GitHub token**: 60 requests per hour
- **With GitHub token**: 5000 requests per hour
- **Authenticated users**: 1000 requests per hour

Rate limit headers:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
```

---

## Webhooks

### Repository Analysis Webhook

Receive notifications when analysis completes.

**Webhook URL Configuration:**
Set in user settings or via API.

**Payload:**
```json
{
  "event": "analysis.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "repository": "user/repo",
    "overall_risk": 0.65,
    "high_risk_files": 12
  }
}
```

---

## SDK Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000"
TOKEN = "your_jwt_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Analyze repository
response = requests.post(
    f"{API_BASE}/analyze-github-url",
    json={"github_url": "facebook/react"},
    headers=headers
)

result = response.json()
print(f"Risk Score: {result['overall_repository_risk']}")
```

### JavaScript

```javascript
const API_BASE = 'http://localhost:8000';
const TOKEN = 'your_jwt_token';

async function analyzeRepository(repoUrl) {
  const response = await fetch(`${API_BASE}/analyze-github-url`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ github_url: repoUrl })
  });
  
  return await response.json();
}

analyzeRepository('facebook/react')
  .then(result => console.log('Risk Score:', result.overall_repository_risk));
```

---

## Versioning

API version is included in the response headers:

```http
X-API-Version: 1.0.0
```

Breaking changes will result in a new major version.

---

## Support

For API support:
- GitHub Issues: https://github.com/nomanqadri34/github-bug-detection/issues
- Email: support@example.com
- Documentation: https://docs.example.com
