import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FiGithub, FiShield, FiZap, FiTrendingUp } from 'react-icons/fi';
import toast from 'react-hot-toast';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import './LoginPage.css';

const LoginPage = ({ onBack, onClassicView }) => {
    const { login, isAuthenticated } = useAuthStore();
    const [isLoading, setIsLoading] = useState(false);
    const [isProcessingCallback, setIsProcessingCallback] = useState(false);

    useEffect(() => {
        // Check for OAuth callback - prevent duplicate calls
        const params = new URLSearchParams(window.location.search);
        const code = params.get('code');

        console.log('🔍 LoginPage mounted - Code:', code ? 'Present' : 'None', 'Authenticated:', isAuthenticated);

        // If already authenticated, don't process callback again
        if (isAuthenticated) {
            console.log('✅ Already authenticated, skipping callback processing');
            return;
        }

        if (code && !sessionStorage.getItem('oauth_processing')) {
            console.log('🔑 OAuth code detected, processing...');
            setIsProcessingCallback(true);
            sessionStorage.setItem('oauth_processing', 'true');
            handleOAuthCallback(code);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleOAuthCallback = async (code) => {
        try {
            console.log('🔄 Processing OAuth callback with code:', code.substring(0, 10) + '...');

            const response = await fetch(`${API_URL}/auth/callback?code=${code}`, {
                method: 'POST'
            });

            console.log('📡 Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ Auth callback failed:', errorText);
                sessionStorage.removeItem('oauth_processing');
                setIsProcessingCallback(false);
                toast.error('Authentication failed. Please try again.');
                window.history.replaceState({}, document.title, '/');
                return;
            }

            const data = await response.json();
            console.log('✅ Auth callback successful! User:', data.user?.login || data.user?.username);

            // Update auth store
            login(data.user, data.token, data.github_token);

            // Clear flags
            sessionStorage.removeItem('oauth_processing');

            // Show success message
            toast.success('Successfully logged in!');

            // Force immediate reload to dashboard
            console.log('🔄 Reloading to dashboard...');
            window.location.href = '/';

        } catch (error) {
            console.error('❌ OAuth error:', error);
            sessionStorage.removeItem('oauth_processing');
            setIsProcessingCallback(false);
            toast.error('Login failed. Please try again.');
            window.history.replaceState({}, document.title, '/');
        }
    };

    const handleGitHubLogin = async () => {
        try {
            setIsLoading(true);
            const response = await fetch(`${API_URL}/auth/github`);

            if (response.status === 503) {
                toast.error('Enhanced features not installed. Using classic mode.');
                setIsLoading(false);
                window.location.href = '/?classic=true';
                return;
            }

            const data = await response.json();
            // Keep loading state while redirecting to GitHub
            window.location.href = data.authorization_url;
        } catch (error) {
            setIsLoading(false);
            toast.error('Failed to initiate login');
            console.error(error);
        }
    };

    return (
        <div className="login-page">
            {isProcessingCallback && (
                <div className="processing-overlay">
                    <div className="processing-content">
                        <div className="spinner-large"></div>
                        <h2>Processing Authentication...</h2>
                        <p>Please wait while we log you in</p>
                    </div>
                </div>
            )}
            <div className="login-container">
                <motion.div
                    className="login-card"
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="login-header">
                        {onBack && (
                            <button onClick={onBack} className="back-btn">
                                ← Back to Classic View
                            </button>
                        )}
                        <FiShield size={48} className="logo-icon" />
                        <h1>Github Bug Detection System</h1>
                        <p>AI-Powered Code Analysis & Bug Detection</p>
                    </div>

                    <div className="features">
                        <div className="feature">
                            <FiZap />
                            <span>Gemini AI Analysis</span>
                        </div>
                        <div className="feature">
                            <FiTrendingUp />
                            <span>Risk Prediction</span>
                        </div>
                        <div className="feature">
                            <FiShield />
                            <span>Security Insights</span>
                        </div>
                    </div>

                    <button
                        className="github-login-btn"
                        onClick={handleGitHubLogin}
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <div className="spinner"></div>
                                <span>Connecting...</span>
                            </>
                        ) : (
                            <>
                                <FiGithub size={20} />
                                <span>Continue with GitHub</span>
                            </>
                        )}
                    </button>

                    {onClassicView && (
                        <button className="classic-view-btn" onClick={onClassicView}>
                            Switch to Classic View
                        </button>
                    )}

                    <p className="login-footer">
                        Secure authentication via GitHub OAuth
                    </p>
                </motion.div>

                <motion.div
                    className="info-section"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <h2>Why Github Bug Detection System?</h2>
                    <ul>
                        <li>🤖 <strong>Gemini AI Integration</strong> - Deep code analysis with Google's latest AI</li>
                        <li>📊 <strong>Professional Dashboard</strong> - Beautiful analytics and insights</li>
                        <li>🔐 <strong>Secure Authentication</strong> - GitHub OAuth integration</li>
                        <li>📈 <strong>Trend Analysis</strong> - Track risk over time</li>
                        <li>👥 <strong>User Management</strong> - Personal profile and history</li>
                        <li>🎨 <strong>Modern UI</strong> - Smooth animations and responsive design</li>
                    </ul>
                </motion.div>
            </div>
        </div>
    );
};

export default LoginPage;
