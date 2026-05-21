import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiMail, FiMapPin, FiBriefcase, FiCalendar } from 'react-icons/fi';
import useAuthStore from '../store/authStore';
import { API_URL } from '../config';
import './UserProfile.css';

const UserProfile = () => {
    const { user } = useAuthStore();
    const [profile, setProfile] = useState(null);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProfile();

        // Auto-refresh every 10 seconds for real-time updates
        const interval = setInterval(fetchProfile, 10000);
        return () => clearInterval(interval);
    }, [user]);

    const fetchProfile = async () => {
        try {
            if (!user?.id) return;

            setLoading(true);

            // Fetch user profile
            const profileResponse = await fetch(`${API_URL}/user/${user.id}`);
            const profileData = await profileResponse.json();

            // Fetch user stats
            const statsResponse = await fetch(`${API_URL}/user/${user.id}/stats`);
            const statsData = await statsResponse.json();

            setProfile(profileData);
            setStats(statsData);
        } catch (error) {
            console.error('Failed to fetch profile:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading || !profile) {
        return <div className="loading">Loading profile...</div>;
    }

    return (
        <div className="user-profile">
            <motion.div
                className="profile-header"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <img src={profile.avatar_url} alt={profile.username} className="profile-avatar" />
                <div className="profile-info">
                    <h2>{profile.name || profile.username}</h2>
                    <p className="username">@{profile.username}</p>
                    {profile.bio && <p className="bio">{profile.bio}</p>}
                </div>
            </motion.div>

            <div className="profile-details">
                <motion.div
                    className="detail-card"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    {profile.email && (
                        <div className="detail-item">
                            <FiMail />
                            <span>{profile.email}</span>
                        </div>
                    )}
                    {profile.location && (
                        <div className="detail-item">
                            <FiMapPin />
                            <span>{profile.location}</span>
                        </div>
                    )}
                    {profile.company && (
                        <div className="detail-item">
                            <FiBriefcase />
                            <span>{profile.company}</span>
                        </div>
                    )}
                    {profile.created_at && (
                        <div className="detail-item">
                            <FiCalendar />
                            <span>Member since {new Date(profile.created_at).toLocaleDateString()}</span>
                        </div>
                    )}
                </motion.div>

                <motion.div
                    className="stats-card"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <h3>Statistics</h3>
                    {stats && (
                        <div className="stats-grid">
                            <div className="stat-item">
                                <span className="stat-label">Total Analyses</span>
                                <span className="stat-value">{stats.total_analyses || 0}</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-label">Repositories</span>
                                <span className="stat-value">{stats.repositories_analyzed || 0}</span>
                            </div>
                            <div className="stat-item">
                                <span className="stat-label">Average Risk</span>
                                <span className="stat-value">{((stats.average_risk || 0) * 100).toFixed(0)}%</span>
                            </div>
                            {stats.last_analysis && (
                                <div className="stat-item">
                                    <span className="stat-label">Last Analysis</span>
                                    <span className="stat-value">{new Date(stats.last_analysis).toLocaleDateString()}</span>
                                </div>
                            )}
                        </div>
                    )}
                </motion.div>
            </div>
        </div>
    );
};

const getRiskLevel = (score) => {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
};

export default UserProfile;
