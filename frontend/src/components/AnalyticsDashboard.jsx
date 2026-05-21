import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiActivity, FiAlertCircle } from 'react-icons/fi';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
    const { user } = useAuthStore();
    const [trends, setTrends] = useState(null);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchAnalytics();

        // Auto-refresh every 10 seconds for real-time updates
        const interval = setInterval(fetchAnalytics, 10000);
        return () => clearInterval(interval);
    }, [user]);

    const fetchAnalytics = async () => {
        try {
            if (!user?.id) return;

            setLoading(true);

            // Fetch user trends
            const trendsResponse = await fetch(`${API_URL}/analytics/trends?user_id=${user.id}`);
            const trendsData = await trendsResponse.json();

            // Fetch user stats
            const statsResponse = await fetch(`${API_URL}/user/${user.id}/stats`);
            const statsData = await statsResponse.json();

            setTrends(trendsData);
            setStats(statsData);
        } catch (error) {
            console.error('Failed to fetch analytics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="loading">Loading analytics...</div>;
    }

    const chartData = trends?.labels?.map((label, index) => ({
        date: label,
        risk: (trends.risk_scores[index] * 100).toFixed(0),
        name: trends.repository_names[index]
    })) || [];

    return (
        <div className="analytics-dashboard">
            <div className="analytics-header">
                <h2>Analytics & Trends</h2>
                <button onClick={fetchAnalytics} className="refresh-btn" title="Refresh data">
                    <FiActivity /> Real-time
                </button>
            </div>

            <div className="stats-grid">
                <motion.div
                    className="stat-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <div className="stat-icon" style={{ background: '#667eea' }}>
                        <FiActivity />
                    </div>
                    <div className="stat-content">
                        <h3>Total Analyses</h3>
                        <p className="stat-value">{stats?.total_analyses || 0}</p>
                    </div>
                </motion.div>

                <motion.div
                    className="stat-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="stat-icon" style={{ background: '#48bb78' }}>
                        <FiTrendingUp />
                    </div>
                    <div className="stat-content">
                        <h3>Repositories</h3>
                        <p className="stat-value">{stats?.repositories_analyzed || 0}</p>
                    </div>
                </motion.div>

                <motion.div
                    className="stat-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <div className="stat-icon" style={{ background: '#f56565' }}>
                        <FiAlertCircle />
                    </div>
                    <div className="stat-content">
                        <h3>Average Risk</h3>
                        <p className="stat-value">{((stats?.average_risk || 0) * 100).toFixed(0)}%</p>
                    </div>
                </motion.div>
            </div>

            {chartData.length > 0 && (
                <motion.div
                    className="chart-container"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <h3>Risk Trend Over Time</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="risk" stroke="#667eea" strokeWidth={2} />
                        </LineChart>
                    </ResponsiveContainer>
                </motion.div>
            )}

            {chartData.length > 0 && (
                <motion.div
                    className="chart-container"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                >
                    <h3>Repository Risk Comparison</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="risk" fill="#764ba2" />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>
            )}

            {chartData.length === 0 && (
                <div className="empty-state">
                    <p>No analysis data yet. Start analyzing repositories to see trends!</p>
                </div>
            )}
        </div>
    );
};

export default AnalyticsDashboard;
