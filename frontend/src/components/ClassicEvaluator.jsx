import React, { useState } from 'react';
import { FiArrowLeft, FiGithub, FiZap, FiLock } from 'react-icons/fi';
import { API_URL } from '../config';
import AnalysisResults from './AnalysisResults';
import './ClassicEvaluator.css';

const ClassicEvaluator = ({ onBackToDashboard }) => {
    const [repoUrl, setRepoUrl] = useState('');
    const [token, setToken] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleEvaluate = async () => {
        if (!repoUrl) {
            setError('Please enter a repository URL');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            // Use the same blazing fast endpoint as the main dashboard
            const response = await fetch(`${API_URL}/analyze-enhanced`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repo_url: repoUrl,
                    access_token: token || localStorage.getItem('github_token') || null,
                    max_commits: 1 // fast analysis
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Analysis failed. Please try again.');
            }

            setResult(data);
        } catch (err) {
            console.error('Analysis error:', err);
            setError(err.message || 'Failed to analyze repository. Check URL or authentication.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className="classic-evaluator-container">
                <button className="back-btn" onClick={onBackToDashboard}>
                    <FiArrowLeft /> Back
                </button>

                <div className="classic-header">
                    <h1>Classic Evaluator</h1>
                    <p>Professional Analysis • Lightning Fast</p>
                </div>

                <div className="evaluator-card">
                    <div className="input-group">
                        <label className="input-label"><FiGithub /> Repository URL</label>
                        <input
                            type="text"
                            className="premium-input"
                            placeholder="e.g., https://github.com/owner/repository"
                            value={repoUrl}
                            onChange={(e) => setRepoUrl(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label"><FiLock /> Access Token (Optional for Private Repos)</label>
                        <input
                            type="password"
                            className="premium-input"
                            placeholder="GitHub Personal Access Token"
                            value={token}
                            onChange={(e) => setToken(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    {error && (
                        <div className="error-box" style={{
                            background: 'rgba(248, 81, 73, 0.12)',
                            border: '1px solid rgba(248, 81, 73, 0.3)',
                            padding: '16px',
                            borderRadius: '12px',
                            color: '#ff7b72',
                            marginBottom: '24px',
                            textAlign: 'center',
                            fontSize: '14px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px'
                        }}>
                            {error}
                        </div>
                    )}

                    {!loading && (
                        <button
                            className="evaluate-btn"
                            onClick={handleEvaluate}
                            disabled={loading || !repoUrl}
                        >
                            <FiZap /> Evaluate Repository
                        </button>
                    )}

                    {loading && (
                        <div className="loading-state">
                            <div className="spinner"></div>
                            <p className="loading-text">Analyzing repository in under 15s...</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Render the EXACT same beautiful 5-tab dashboard when result is ready */}
            {result && (
                <AnalysisResults 
                    result={result} 
                    onClose={() => setResult(null)} 
                />
            )}
        </>
    );
};

export default ClassicEvaluator;
