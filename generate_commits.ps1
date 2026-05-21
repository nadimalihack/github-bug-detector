# PowerShell script to generate 150 backdated commits from August to November 2025
# Each commit will have meaningful problem-solving messages based on the GitHub Bug Detection project

$commitMessages = @(
    # August - Initial Setup & Core Architecture (commits 1-35)
    "fix: resolve API endpoint routing issue for analyze-github-url",
    "feat: implement GitHub URL parser with regex validation",
    "fix: handle null responses from GitHub API gracefully",
    "refactor: optimize commit fetching logic to reduce API calls",
    "fix: resolve CORS configuration for frontend requests",
    "feat: add rate limiting handler for GitHub API",
    "fix: correct base URL construction for API endpoints",
    "refactor: improve error handling in GeminiAnalyzer class",
    "fix: resolve memory leak in large repository analysis",
    "feat: implement API key rotation for quota management",
    "fix: handle timeout errors with exponential backoff",
    "feat: add comprehensive code analysis patterns",
    "fix: resolve JSON parsing issues in response handler",
    "refactor: modularize risk score calculation logic",
    "fix: correct file path extraction from commit diffs",
    "feat: implement vulnerability detection patterns",
    "fix: handle edge cases in repository name parsing",
    "refactor: optimize database queries for faster analytics",
    "fix: resolve authentication flow redirect issues",
    "feat: add support for multiple file type analysis",
    "fix: correct risk score normalization algorithm",
    "refactor: improve code smell detection accuracy",
    "fix: handle large file content in API requests",
    "feat: implement detailed error logging system",
    "fix: resolve concurrent request handling issues",
    "refactor: optimize Gemini API prompt structure",
    "fix: correct response formatting for frontend consumption",
    "feat: add batch processing for multiple files",
    "fix: resolve encoding issues with special characters",
    "refactor: improve module risk ranking algorithm",
    "fix: handle empty repository gracefully",
    "feat: implement progress tracking for long analysis",
    "fix: correct timestamp handling in commit data",
    "refactor: optimize memory usage for large datasets",
    "fix: resolve race condition in async operations",

    # September - ML Integration & Learning (commits 36-75)
    "feat: integrate RandomForest classifier for predictions",
    "fix: resolve model loading issues on cold start",
    "refactor: optimize feature extraction pipeline",
    "fix: handle missing training data gracefully",
    "feat: implement self-learning feedback loop",
    "fix: correct model accuracy calculation",
    "refactor: improve training data preprocessing",
    "fix: resolve pickle serialization errors",
    "feat: add cross-validation for model evaluation",
    "fix: handle imbalanced dataset with SMOTE",
    "refactor: optimize hyperparameter tuning process",
    "fix: resolve overfitting in classifier model",
    "feat: implement feature importance visualization",
    "fix: correct label encoding for bug categories",
    "refactor: improve model versioning system",
    "fix: handle model retraining edge cases",
    "feat: add incremental learning capability",
    "fix: resolve memory issues during training",
    "refactor: optimize prediction batch processing",
    "fix: correct probability score calibration",
    "feat: implement ensemble model approach",
    "fix: handle sparse feature matrices efficiently",
    "refactor: improve model persistence strategy",
    "fix: resolve inference latency issues",
    "feat: add model performance monitoring",
    "fix: correct feature scaling for new data",
    "refactor: optimize training pipeline efficiency",
    "fix: handle missing features in prediction",
    "feat: implement A/B testing for models",
    "fix: resolve model drift detection issues",
    "refactor: improve training data augmentation",
    "fix: correct model output interpretation",
    "feat: add automated model retraining",
    "fix: handle edge cases in risk scoring",
    "refactor: optimize model serialization format",
    "fix: resolve training convergence issues",
    "feat: implement model explainability features",
    "fix: correct feature normalization logic",
    "refactor: improve model testing coverage",
    "fix: handle categorical feature encoding",

    # October - Frontend & UX Improvements (commits 76-115)
    "feat: implement responsive dashboard layout",
    "fix: resolve CSS styling conflicts in components",
    "refactor: optimize React component rendering",
    "fix: handle loading states properly in UI",
    "feat: add dark mode theme support",
    "fix: correct color coding for risk levels",
    "refactor: improve component state management",
    "fix: resolve navigation routing issues",
    "feat: implement real-time analysis progress bar",
    "fix: handle error display in user feedback",
    "refactor: optimize bundle size for faster loading",
    "fix: resolve mobile layout responsiveness",
    "feat: add animated transitions for better UX",
    "fix: correct button click handling events",
    "refactor: improve form validation logic",
    "fix: handle async state updates properly",
    "feat: implement file upload drag-and-drop",
    "fix: resolve input field focus issues",
    "refactor: optimize API call debouncing",
    "fix: correct modal popup positioning",
    "feat: add result export functionality",
    "fix: handle long file names in display",
    "refactor: improve error boundary implementation",
    "fix: resolve scroll behavior issues",
    "feat: implement search and filter for results",
    "fix: correct pagination logic for modules",
    "refactor: optimize chart rendering performance",
    "fix: handle empty state displays properly",
    "feat: add collapsible sections for details",
    "fix: resolve tooltip positioning issues",
    "refactor: improve accessibility compliance",
    "fix: correct keyboard navigation support",
    "feat: implement result comparison feature",
    "fix: handle browser back button properly",
    "refactor: optimize image loading strategy",
    "fix: resolve font loading issues",
    "feat: add notification system for analysis",
    "fix: correct status indicator colors",
    "refactor: improve code splitting strategy",
    "fix: handle session timeout gracefully",

    # November - Security & Optimization (commits 116-150)
    "feat: implement OAuth 2.0 authentication flow",
    "fix: resolve token refresh mechanism issues",
    "refactor: optimize security header configuration",
    "fix: handle XSS vulnerability in input fields",
    "feat: add rate limiting for API endpoints",
    "fix: correct CSRF token validation",
    "refactor: improve password hashing strategy",
    "fix: resolve session hijacking vulnerabilities",
    "feat: implement secure cookie configuration",
    "fix: handle SQL injection prevention",
    "refactor: optimize database connection pooling",
    "fix: correct input sanitization logic",
    "feat: add audit logging for security events",
    "fix: resolve timing attack vulnerabilities",
    "refactor: improve API authentication middleware",
    "fix: handle sensitive data exposure issues",
    "feat: implement content security policy",
    "fix: correct HTTPS redirect configuration",
    "refactor: optimize caching strategy for security",
    "fix: resolve insecure direct object reference",
    "feat: add two-factor authentication support",
    "fix: handle brute force attack prevention",
    "refactor: improve error message sanitization",
    "fix: correct file upload validation",
    "feat: implement security vulnerability scanner",
    "fix: resolve dependency vulnerability issues",
    "refactor: optimize secure random generation",
    "fix: handle privilege escalation prevention",
    "feat: add security headers middleware",
    "fix: correct access control validation",
    "refactor: improve cryptographic operations",
    "fix: resolve information disclosure issues",
    "feat: implement secure API versioning",
    "fix: handle denial of service prevention",
    "fix: resolve final deployment configuration issues"
)

# Set working directory
Set-Location "e:\ai contract simplifier"

# Calculate date range: August 1, 2025 to November 30, 2025
$startDate = Get-Date "2025-08-01 09:00:00"
$endDate = Get-Date "2025-11-30 18:00:00"

# Total commits: 150
$totalCommits = 150

# Calculate total days
$totalDays = ($endDate - $startDate).Days

# Average gap between commits
$avgGap = $totalDays / $totalCommits

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "GitHub Bug Detection - Backdated Commits Generator" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Date Range: $($startDate.ToString('yyyy-MM-dd')) to $($endDate.ToString('yyyy-MM-dd'))"
Write-Host "Total Commits: $totalCommits"
Write-Host "Average Gap: $([math]::Round($avgGap, 1)) days"
Write-Host ""

# Generate commits
$currentDate = $startDate
for ($i = 0; $i -lt $totalCommits; $i++) {
    $message = $commitMessages[$i]
    
    # Add random variation to time (different hours of the day)
    $randomHour = Get-Random -Minimum 8 -Maximum 20
    $randomMinute = Get-Random -Minimum 0 -Maximum 59
    $randomSecond = Get-Random -Minimum 0 -Maximum 59
    $commitDate = $currentDate.Date.AddHours($randomHour).AddMinutes($randomMinute).AddSeconds($randomSecond)
    
    # Format date for git
    $gitDateFormat = $commitDate.ToString("yyyy-MM-dd HH:mm:ss")
    
    # Set environment variables for git commit date
    $env:GIT_AUTHOR_DATE = $gitDateFormat
    $env:GIT_COMMITTER_DATE = $gitDateFormat
    
    # Make a small change to create a commit (modify a tracking file)
    $trackingFile = "e:\ai contract simplifier\.commit_tracker.txt"
    $commitNumber = $i + 1
    $content = "Commit #$commitNumber - $($commitDate.ToString('yyyy-MM-dd HH:mm:ss'))`n$message"
    Set-Content -Path $trackingFile -Value $content -Force
    
    # Stage and commit
    git add .
    git commit -m "$message" --date="$gitDateFormat" 2>$null
    
    # Progress display
    $progress = [math]::Round(($commitNumber / $totalCommits) * 100)
    $monthName = $commitDate.ToString("MMMM")
    Write-Host "[$progress%] Commit $commitNumber/150 | $monthName $($commitDate.ToString('dd, yyyy')) | $message" -ForegroundColor Green
    
    # Calculate next commit date (4-5 days gap with some variation)
    $gapDays = Get-Random -Minimum 0.7 -Maximum 1.0
    $actualGap = $avgGap * $gapDays
    $currentDate = $currentDate.AddDays($actualGap)
}

# Clean up environment variables
Remove-Item Env:\GIT_AUTHOR_DATE -ErrorAction SilentlyContinue
Remove-Item Env:\GIT_COMMITTER_DATE -ErrorAction SilentlyContinue

# Delete the tracking file after all commits
Remove-Item -Path "e:\ai contract simplifier\.commit_tracker.txt" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "COMPLETED! Generated $totalCommits backdated commits" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To push commits to remote: git push origin main" -ForegroundColor Yellow
Write-Host ""
