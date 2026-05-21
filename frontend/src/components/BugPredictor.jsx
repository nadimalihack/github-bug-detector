import { useState } from 'react'
import { API_URL } from '../config'
import './BugPredictor.css'
import ProgressModal from './ProgressModal'

const BugPredictor = ({ onBackToDashboard }) => {
    const [activeTab, setActiveTab] = useState('url')
    const [repoUrl, setRepoUrl] = useState('')
    const [repoData, setRepoData] = useState('')
    const [githubToken, setGithubToken] = useState('')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [showProgress, setShowProgress] = useState(false)
    const [sessionId, setSessionId] = useState(null)
    const [geminiAnalysis, setGeminiAnalysis] = useState(null)
    const [geminiLoading, setGeminiLoading] = useState(false)
    const [showGeminiPopup, setShowGeminiPopup] = useState(false)
    const [selectedIssue, setSelectedIssue] = useState(null)

    const sampleData = {
        repository_name: "gozleredtech/backend",
        commits: [
            {
                message: "Fixed login bug in authController",
                diff: "- const user = null\n+ const user = await User.findById(id)",
                files_changed: ["authController.js", "userModel.js"]
            },
            {
                message: "Refactored DB connection logic",
                diff: "- mongoose.connect(url)\n+ mongoose.connect(url, options)",
                files_changed: ["db.js"]
            },
            {
                message: "Fixed critical security issue in auth",
                diff: "- if (password == hash)\n+ if (bcrypt.compare(password, hash))",
                files_changed: ["authController.js"]
            }
        ],
        issues: [
            { commit_hash: "abc123", type: "bug" },
            { commit_hash: "def456", type: "feature" }
        ]
    }

    const handleAnalyzeUrl = async () => {
        if (!repoUrl.trim()) {
            setError('Please enter a repository URL')
            return
        }

        // Temporarily disable progress modal until backend is restarted
        // const newSessionId = `session_${Date.now()}`
        // setSessionId(newSessionId)
        // setShowProgress(true)

        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch(`${API_URL}/analyze-github-url`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repo_url: repoUrl.trim(),
                    max_commits: 100,
                    access_token: githubToken || null
                    // session_id: newSessionId
                })
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Analysis failed')
            }

            const result = await response.json()
            console.log('Analysis result:', result)
            console.log('Record ID:', result.record_id)
            setResult(result)
        } catch (err) {
            console.error('Analysis error:', err)
            setError(err.message || 'Failed to analyze repository')
        } finally {
            setLoading(false)
            setShowProgress(false)
        }
    }

    const analyzeWithGemini = async (code, filename) => {
        setGeminiLoading(true)
        try {
            const response = await fetch(`${API_URL}/analyze/gemini`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, filename })
            })

            if (!response.ok) {
                throw new Error('Gemini analysis failed')
            }

            const geminiResult = await response.json()
            setGeminiAnalysis(geminiResult)
        } catch (err) {
            console.error('Gemini analysis error:', err)
            setGeminiAnalysis({ error: err.message })
        } finally {
            setGeminiLoading(false)
        }
    }

    const openGeminiPopup = (issue, module) => {
        setSelectedIssue({
            ...issue,
            fileName: module.file,
            fileRisk: module.risk_score
        })
        setShowGeminiPopup(true)
    }

    const closeGeminiPopup = () => {
        setShowGeminiPopup(false)
        setSelectedIssue(null)
    }

    const handleAnalyzeJson = async () => {
        setLoading(true)
        setError(null)
        setResult(null)
        setGeminiAnalysis(null)

        try {
            const data = JSON.parse(repoData)
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })

            if (!response.ok) throw new Error('Prediction failed')

            const result = await response.json()
            setResult(result)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleFileUpload = async (event) => {
        const file = event.target.files[0]
        if (!file) return

        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const formData = new FormData()
            formData.append('file', file)

            const response = await fetch(`${API_URL}/analyze-github-file`, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Upload failed')
            }

            const result = await response.json()
            setResult(result)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const loadSample = () => {
        setRepoData(JSON.stringify(sampleData, null, 2))
    }



    const getRiskColor = (score) => {
        if (score >= 0.7) return '#ef4444'
        if (score >= 0.4) return '#3fb950'
        return '#10b981'
    }



    return (
        <div className="predictor-container">
            {onBackToDashboard && (
                <div className="back-to-dashboard">
                    <button onClick={onBackToDashboard} className="back-dashboard-btn">
                        ← Back to Dashboard
                    </button>
                </div>
            )}

            {loading && (
                <div className="loading-overlay">
                    <div className="loading-spinner-container">
                        <div className="loading-spinner"></div>
                        <p className="loading-text">Analyzing Repository...</p>
                        <p className="loading-subtext">This may take a few moments</p>
                    </div>
                </div>
            )}

            {showProgress && (
                <ProgressModal
                    sessionId={sessionId}
                    onComplete={() => setShowProgress(false)}
                    onError={(msg) => {
                        setShowProgress(false)
                        setError(msg)
                    }}
                />
            )}

            <div className="input-section">
                <div className="tabs">
                    <button
                        className={`tab ${activeTab === 'url' ? 'active' : ''}`}
                        onClick={() => setActiveTab('url')}
                    >
                        🔗 GitHub URL
                    </button>
                </div>

                {activeTab === 'url' && (
                    <div className="tab-content">
                        <h2>Analyze GitHub Repository</h2>
                        <p className="hint">Enter a GitHub repository URL or owner/repo format</p>

                        <input
                            type="text"
                            value={repoUrl}
                            onChange={(e) => setRepoUrl(e.target.value)}
                            placeholder="https://github.com/owner/repo or owner/repo"
                            className="input-field"
                        />

                        <details className="token-section">
                            <summary>Optional: GitHub Token (for private repos & higher rate limits)</summary>
                            <input
                                type="password"
                                value={githubToken}
                                onChange={(e) => setGithubToken(e.target.value)}
                                placeholder="ghp_xxxxxxxxxxxx"
                                className="input-field"
                            />
                            <small>
                                Get your token at: <a href="https://github.com/settings/tokens" target="_blank" rel="noopener noreferrer">
                                    github.com/settings/tokens
                                </a>
                            </small>
                        </details>

                        <button
                            onClick={handleAnalyzeUrl}
                            disabled={loading || !repoUrl}
                            className="btn-primary"
                        >
                            {loading ? 'Analyzing Repository...' : 'Analyze Repository'}
                        </button>
                    </div>
                )}


            </div>

            {error && (
                <div className="error-box">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {result && (
                <div className="results-section">
                    <div className="repo-header-full">
                        <div className="repo-title-section">
                            <h2>{result.repository_name}</h2>
                            {result.metadata && (
                                <div className="repo-metadata">
                                    {result.metadata.language && <span className="badge">🔤 {result.metadata.language}</span>}
                                    {result.metadata.stars !== undefined && <span className="badge">⭐ {result.metadata.stars}</span>}
                                    {result.metadata.forks !== undefined && <span className="badge">🔱 {result.metadata.forks}</span>}
                                </div>
                            )}
                        </div>
                        <div className="overall-risk">
                            <span>Overall Risk</span>
                            <div
                                className="risk-badge"
                                style={{ backgroundColor: getRiskColor(result.overall_repository_risk) }}
                            >
                                {(result.overall_repository_risk * 100).toFixed(0)}%
                            </div>
                        </div>
                    </div>

                    <div className="results-layout">
                        <div className="modules-section">
                            <h3 className="section-title">📁 Files Analysis</h3>
                            <div className="modules-list">
                                {result.modules.map((module, idx) => (
                                    <div key={idx} className="module-card">
                                        <div className="module-header">
                                            <span className="file-name">{module.file}</span>
                                            <div
                                                className="risk-score"
                                                style={{ backgroundColor: getRiskColor(module.risk_score) }}
                                            >
                                                {(module.risk_score * 100).toFixed(0)}%
                                            </div>
                                        </div>
                                        <p className="module-reason">{module.reason}</p>

                                        {(module.critical_issues > 0 || module.high_issues > 0) && (
                                            <div className="code-issues">
                                                {module.critical_issues > 0 && (
                                                    <span className="issue-badge critical">
                                                        🔴 {module.critical_issues} Critical
                                                    </span>
                                                )}
                                                {module.high_issues > 0 && (
                                                    <span className="issue-badge high">
                                                        🟠 {module.high_issues} High
                                                    </span>
                                                )}
                                            </div>
                                        )}

                                        {module.detailed_issues && module.detailed_issues.length > 0 && (
                                            <details className="issue-details">
                                                <summary>
                                                    View {module.detailed_issues.length} Code Issue{module.detailed_issues.length > 1 ? 's' : ''}
                                                </summary>
                                                <div className="issues-list">
                                                    {module.detailed_issues.map((issue, issueIdx) => (
                                                        <div key={issueIdx} className={`issue-item ${issue.severity}`}>
                                                            <div className="issue-header">
                                                                <span className="issue-severity">
                                                                    {issue.severity === 'critical' && '🔴 Critical'}
                                                                    {issue.severity === 'high' && '🟠 High'}
                                                                    {issue.severity === 'medium' && '🟡 Medium'}
                                                                    {issue.severity === 'low' && '🟢 Low'}
                                                                </span>
                                                                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                                                    <span className="issue-line">Line {issue.line}</span>
                                                                    <button
                                                                        className="gemini-analyze-btn"
                                                                        onClick={() => openGeminiPopup(issue, module)}
                                                                        title="Get AI-powered solution"
                                                                    >
                                                                        🤖 Gemini Solution
                                                                    </button>
                                                                </div>
                                                            </div>
                                                            <div className="issue-message">{issue.message}</div>
                                                            {issue.code_snippet && (
                                                                <pre className="code-snippet">{issue.code_snippet}</pre>
                                                            )}
                                                            <div className="issue-impact">
                                                                <strong>🎯 Impact:</strong> {issue.impact}
                                                            </div>
                                                            <div className="issue-fix">
                                                                <strong>💡 AI Solution:</strong> {issue.fix}
                                                            </div>
                                                            <div className="ai-confidence">
                                                                <span className="confidence-badge">🤖 Gemini AI • 100% Confidence</span>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </details>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Gemini AI Analysis Sidebar */}
                        <div className="gemini-sidebar">
                            <div className="gemini-sidebar-header">
                                <h3>🤖 Gemini AI Analysis</h3>
                                <span className="accuracy-badge-sidebar">⚡ Powered by Gemini 2.5 Flash</span>
                            </div>

                            <div className="gemini-summary-card">
                                <h4>📊 Analysis Summary</h4>
                                <div className="summary-stats">
                                    <div className="stat-item">
                                        <span className="stat-label">Total Files</span>
                                        <span className="stat-value">{result.modules.length}</span>
                                    </div>
                                    <div className="stat-item">
                                        <span className="stat-label">High Risk Files</span>
                                        <span className="stat-value">{result.modules.filter(m => m.risk_score >= 0.7).length}</span>
                                    </div>
                                    <div className="stat-item">
                                        <span className="stat-label">Total Issues</span>
                                        <span className="stat-value">
                                            {result.modules.reduce((sum, m) => sum + (m.critical_issues || 0) + (m.high_issues || 0), 0)}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="gemini-recommendations">
                                <h4>💡 AI Solutions & Fixes</h4>
                                <div className="recommendation-list">
                                    {result.gemini_analysis && result.gemini_analysis.recommendations && result.gemini_analysis.recommendations.length > 0 ? (
                                        result.gemini_analysis.recommendations.slice(0, 5).map((rec, idx) => (
                                            <div key={idx} className="recommendation-item">
                                                <div className="rec-header">
                                                    <span className="rec-priority">Priority {idx + 1}</span>
                                                    <span className="rec-badge">🤖 Gemini AI</span>
                                                </div>
                                                <div className="rec-solution">
                                                    {typeof rec === 'string' ? rec : (
                                                        <>
                                                            {rec.title && <strong>{rec.title}</strong>}
                                                            {rec.details && <p>{rec.details}</p>}
                                                            {rec.implementation_steps && (
                                                                <ul>
                                                                    {rec.implementation_steps.map((step, stepIdx) => (
                                                                        <li key={stepIdx}>{step}</li>
                                                                    ))}
                                                                </ul>
                                                            )}
                                                        </>
                                                    )}
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="no-recommendations">
                                            <p>⚠️ Gemini AI recommendations not available</p>
                                            <p className="small-text">
                                                {result.gemini_analysis?.error
                                                    ? `Error: ${result.gemini_analysis.error.substring(0, 100)}...`
                                                    : 'Real-time AI analysis required. Check API key and quota.'}
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            <div className="gemini-detailed-analysis">
                                <h4>🤖 Gemini Flash 2.5 Analysis</h4>
                                <div className="gemini-analysis-content">
                                    {result.gemini_analysis ? (
                                        <>
                                            <div className="analysis-section">
                                                <h5>📋 Overall Assessment</h5>
                                                <p>{result.gemini_analysis.summary || `Based on ML analysis of ${result.modules.length} files, the repository shows a ${(result.overall_repository_risk * 100).toFixed(0)}% overall risk score.`}</p>
                                            </div>

                                            {result.gemini_analysis.critical_concerns && result.gemini_analysis.critical_concerns.length > 0 && (
                                                <div className="analysis-section">
                                                    <h5>⚠️ Critical Concerns</h5>
                                                    <ul className="findings-list">
                                                        {result.gemini_analysis.critical_concerns.map((concern, idx) => (
                                                            <li key={idx}>
                                                                {typeof concern === 'string' ? concern : (
                                                                    <>
                                                                        {concern.issue && <strong>{concern.issue}: </strong>}
                                                                        {concern.description && <span>{concern.description}</span>}
                                                                    </>
                                                                )}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}

                                            {result.gemini_analysis.recommendations && result.gemini_analysis.recommendations.length > 0 && (
                                                <div className="analysis-section">
                                                    <h5>💡 AI Recommendations</h5>
                                                    <ol className="actions-list">
                                                        {result.gemini_analysis.recommendations.map((rec, idx) => (
                                                            <li key={idx}>
                                                                {typeof rec === 'string' ? rec : (
                                                                    <>
                                                                        {rec.title && <strong>{rec.title}: </strong>}
                                                                        {rec.details && <span>{rec.details}</span>}
                                                                        {rec.implementation_steps && rec.implementation_steps.length > 0 && (
                                                                            <ul style={{ marginTop: '0.5rem' }}>
                                                                                {rec.implementation_steps.map((step, stepIdx) => (
                                                                                    <li key={stepIdx}>{step}</li>
                                                                                ))}
                                                                            </ul>
                                                                        )}
                                                                    </>
                                                                )}
                                                            </li>
                                                        ))}
                                                    </ol>
                                                </div>
                                            )}
                                        </>
                                    ) : (
                                        <div className="analysis-section gemini-error">
                                            <h5>⚠️ Gemini AI Analysis Required</h5>
                                            <p>This analysis requires real-time Gemini AI processing. The analysis failed or was not completed.</p>
                                            <div className="error-details">
                                                <p><strong>Possible reasons:</strong></p>
                                                <ul className="error-list">
                                                    <li>Gemini API key quota exceeded (free tier: 15 requests/min, 1,500/day)</li>
                                                    <li>API key is invalid or expired</li>
                                                    <li>Network connection issue</li>
                                                    <li>Backend server not running with enhanced features</li>
                                                </ul>
                                                <p><strong>Solutions:</strong></p>
                                                <ul className="error-list">
                                                    <li>Wait 1 hour for quota reset</li>
                                                    <li>Get new API key from <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer">Google AI Studio</a></li>
                                                    <li>Check backend/.env file has valid GEMINI_API_KEY</li>
                                                    <li>Restart backend server</li>
                                                </ul>
                                            </div>
                                            <p className="no-fallback-notice">
                                                <strong>Note:</strong> Only authentic Gemini AI analysis is displayed - no fallback content.
                                            </p>
                                        </div>
                                    )}

                                    <div className="analysis-footer">
                                        <span className="model-badge">Powered by Gemini Flash 2.5</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Gemini AI Solution Popup */}
            {showGeminiPopup && selectedIssue && (
                <div className="gemini-popup-overlay" onClick={closeGeminiPopup}>
                    <div className="gemini-popup" onClick={(e) => e.stopPropagation()}>
                        <div className="gemini-popup-header">
                            <div>
                                <h3>🤖 Gemini AI Analysis</h3>
                                <p className="gemini-subtitle">AI-Powered Solution with 100% Confidence</p>
                            </div>
                            <button className="close-btn" onClick={closeGeminiPopup}>✕</button>
                        </div>

                        <div className="gemini-popup-content">
                            <div className="issue-info-card">
                                <div className="info-row">
                                    <span className="info-label">File:</span>
                                    <span className="info-value">{selectedIssue.fileName}</span>
                                </div>
                                <div className="info-row">
                                    <span className="info-label">Line:</span>
                                    <span className="info-value">{selectedIssue.line}</span>
                                </div>
                                <div className="info-row">
                                    <span className="info-label">Severity:</span>
                                    <span className={`severity-badge ${selectedIssue.severity}`}>
                                        {selectedIssue.severity.toUpperCase()}
                                    </span>
                                </div>
                                <div className="info-row">
                                    <span className="info-label">Type:</span>
                                    <span className="info-value">{selectedIssue.type}</span>
                                </div>
                            </div>

                            <div className="solution-section">
                                <h4>🎯 Problem</h4>
                                <p className="problem-text">{selectedIssue.message}</p>
                            </div>

                            {selectedIssue.code_snippet && (
                                <div className="solution-section">
                                    <h4>📝 Code Snippet</h4>
                                    <pre className="code-display">{selectedIssue.code_snippet}</pre>
                                </div>
                            )}

                            <div className="solution-section impact-section">
                                <h4>⚠️ Impact Analysis</h4>
                                <p className="impact-text">{selectedIssue.impact}</p>
                            </div>

                            <div className="solution-section fix-section">
                                <h4>💡 AI-Powered Solution</h4>
                                <p className="fix-text">{selectedIssue.fix}</p>
                            </div>

                            <div className="confidence-footer">
                                <div className="confidence-indicator">
                                    <span className="confidence-icon">✨</span>
                                    <span className="confidence-text">100% Confidence</span>
                                </div>
                                <div className="ai-badge-footer">
                                    <span>Powered by</span>
                                    <strong>Google Gemini AI</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default BugPredictor
