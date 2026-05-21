import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiGithub, FiStar, FiGitBranch, FiSearch, FiRefreshCw } from 'react-icons/fi';
import toast from 'react-hot-toast';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import AnalysisResults from './AnalysisResults';
import './RepositoryList.css';

const RepositoryList = ({ onAnalysisComplete }) => {
    const { githubToken, user } = useAuthStore();
    const [repositories, setRepositories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [analyzing, setAnalyzing] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);

    useEffect(() => {
        fetchRepositories();
    }, []);

    const fetchRepositories = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${API_URL}/user/${user.id}/repositories?github_token=${githubToken}`);
            const data = await response.json();
            setRepositories(data.repositories || []);
        } catch (error) {
            toast.error('Failed to fetch repositories');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const analyzeRepository = async (repo) => {
        setAnalyzing(repo.full_name);

        try {
            console.log('Analyzing repository:', repo.full_name, 'for user:', user.id);

            // Try enhanced analysis first, fallback to standard
            let response = await fetch(`${API_URL}/analyze-enhanced`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repo_url: repo.full_name,
                    access_token: githubToken,
                    user_id: user.id
                })
            });

            // If enhanced fails, use standard analysis
            if (!response.ok && response.status === 503) {
                console.log('Enhanced analysis not available, using standard analysis');
                response = await fetch(`${API_URL}/analyze-github-url`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        repo_url: repo.full_name,
                        access_token: githubToken,
                        user_id: user.id
                    })
                });
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const result = await response.json();
            console.log('✅ Analysis complete:', result);
            console.log('📊 Triggering stats refresh for user:', user.id);

            toast.success(`Analysis complete! Risk: ${(result.overall_repository_risk * 100).toFixed(0)}%`);

            // Show results in modal
            setAnalysisResult(result);

            // Force immediate stats refresh - call multiple times to ensure it works
            if (onAnalysisComplete) {
                console.log('🔄 Calling onAnalysisComplete...');
                onAnalysisComplete(); // Immediate
                setTimeout(() => {
                    console.log('🔄 Second refresh...');
                    onAnalysisComplete();
                }, 1000);
                setTimeout(() => {
                    console.log('🔄 Third refresh...');
                    onAnalysisComplete();
                }, 2000);
            }
        } catch (error) {
            const errorMessage = error.message || 'Analysis failed';
            console.error('Analysis error:', error);

            // Show detailed error messages
            if (errorMessage.includes('authentication failed') || errorMessage.includes('Bad credentials')) {
                toast.error('GitHub authentication failed. Please log out and log in again.', { duration: 6000 });
            } else if (errorMessage.includes('not found') || errorMessage.includes('Not Found')) {
                toast.error('Repository not found. Check the name and make sure you have access.', { duration: 6000 });
            } else if (errorMessage.includes('rate limit')) {
                toast.error('GitHub API rate limit exceeded. Please wait a few minutes.', { duration: 6000 });
            } else if (errorMessage.includes('empty')) {
                toast.error('Repository is empty - no commits to analyze');
            } else {
                toast.error(`Analysis failed: ${errorMessage}`, { duration: 5000 });
            }
        } finally {
            setAnalyzing(null);
        }
    };

    const filteredRepos = repositories.filter(repo =>
        repo.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        repo.description?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {
        return <div className="loading">Loading repositories...</div>;
    }

    return (
        <>
            {analyzing && (
                <div className="loading-overlay">
                    <div className="loading-spinner-container">
                        <div className="loading-spinner"></div>
                        <p className="loading-text">Analyzing {analyzing}...</p>
                        <p className="loading-subtext">This may take a few moments</p>
                    </div>
                </div>
            )}

            <div className="repository-list">
                <div className="list-header">
                    <h2>Your Repositories</h2>
                    <button onClick={fetchRepositories} className="refresh-btn">
                        <FiRefreshCw /> Refresh
                    </button>
                </div>

                <div className="search-bar">
                    <FiSearch />
                    <input
                        type="text"
                        placeholder="Search repositories..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="repos-grid">
                    {filteredRepos.map((repo, index) => (
                        <motion.div
                            key={repo.id}
                            className="repo-card"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                        >
                            <div className="repo-header">
                                <FiGithub size={24} />
                                <h3>{repo.name}</h3>
                            </div>

                            <p className="repo-description">
                                {repo.description || 'No description available'}
                            </p>

                            <div className="repo-stats">
                                <span><FiStar /> {repo.stargazers_count || 0}</span>
                                <span><FiGitBranch /> {repo.forks_count || 0}</span>
                                {repo.language && <span className="language">{repo.language}</span>}
                            </div>

                            <button
                                className="analyze-btn"
                                onClick={() => analyzeRepository(repo)}
                                disabled={analyzing === repo.full_name}
                            >
                                {analyzing === repo.full_name ? 'Analyzing...' : 'Analyze'}
                            </button>
                        </motion.div>
                    ))}
                </div>

                {filteredRepos.length === 0 && (
                    <div className="empty-state">
                        <p>No repositories found</p>
                    </div>
                )}
            </div>

            <AnimatePresence>
                {analysisResult && (
                    <AnalysisResults
                        result={analysisResult}
                        onClose={() => setAnalysisResult(null)}
                    />
                )}
            </AnimatePresence>
        </>
    );
};

export default RepositoryList;
