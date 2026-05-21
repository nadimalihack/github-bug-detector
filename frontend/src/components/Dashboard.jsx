import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiGithub, FiLogOut, FiTrendingUp, FiActivity, FiBarChart2 } from 'react-icons/fi';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import AnalyticsDashboard from './AnalyticsDashboard';
import RepositoryList from './RepositoryList';
import UserProfile from './UserProfile';
import './Dashboard.css';

const Dashboard = ({ onClassicView }) => {
    const { user, logout } = useAuthStore();
    const [activeTab, setActiveTab] = useState('repositories');
    const [stats, setStats] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);

    useEffect(() => {
        if (user) {
            fetchUserStats();
            // Auto-refresh stats every 5 seconds for real-time updates
            const interval = setInterval(fetchUserStats, 5000);
            return () => clearInterval(interval);
        }
    }, [user, refreshKey]);

    const fetchUserStats = async () => {
        try {
            if (!user?.id) {
                console.warn('No user ID available');
                return;
            }

            console.log('Fetching stats for user:', user.id);
            const response = await fetch(`${API_URL}/user/${user.id}/stats`);

            if (!response.ok) {
                console.error('Stats fetch failed:', response.status, response.statusText);
                return;
            }

            const data = await response.json();
            console.log('Stats received:', data);
            setStats(data);
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        }
    };

    const refreshStats = () => {
        setRefreshKey(prev => prev + 1);
    };

    return (
        <div className="dashboard">
            <div className="dashboard-content">
                <aside className="sidebar">
                    <nav>
                        <button
                            className={activeTab === 'repositories' ? 'active' : ''}
                            onClick={() => setActiveTab('repositories')}
                        >
                            <FiGithub /> Repositories
                        </button>
                        <button
                            className={activeTab === 'analytics' ? 'active' : ''}
                            onClick={() => setActiveTab('analytics')}
                        >
                            <FiBarChart2 /> Analytics
                        </button>
                        <button
                            className={activeTab === 'profile' ? 'active' : ''}
                            onClick={() => setActiveTab('profile')}
                        >
                            <FiActivity /> Profile
                        </button>
                    </nav>

                    {stats && (
                        <div className="stats-sidebar">
                            <div className="stats-header">
                                <h3>Your Stats</h3>
                                <button
                                    onClick={() => {
                                        console.log('🔄 Manual refresh triggered');
                                        fetchUserStats();
                                    }}
                                    className="refresh-stats-btn"
                                    title="Refresh stats"
                                >
                                    🔄
                                </button>
                            </div>
                            <div className="stat-item">
                                <span>Total Analyses</span>
                                <strong>{stats.total_analyses}</strong>
                            </div>
                            <div className="stat-item">
                                <span>Repositories</span>
                                <strong>{stats.repositories_analyzed}</strong>
                            </div>
                            <div className="stat-item">
                                <span>Avg Risk</span>
                                <strong>{(stats.average_risk * 100).toFixed(0)}%</strong>
                            </div>
                        </div>
                    )}
                </aside>

                <main className="main-content">
                    <motion.div
                        key={activeTab}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                    >
                        {activeTab === 'repositories' && <RepositoryList onAnalysisComplete={refreshStats} />}
                        {activeTab === 'analytics' && <AnalyticsDashboard />}
                        {activeTab === 'profile' && <UserProfile onStatsUpdate={refreshStats} />}
                    </motion.div>
                </main>
            </div>
        </div>
    );
};

export default Dashboard;
