import { useState } from 'react';
import { FiGithub, FiMenu, FiX, FiHome, FiInfo, FiLogIn, FiUser } from 'react-icons/fi';
import useAuthStore from '../store/authStore';
import './Navbar.css';

const Navbar = ({ onNavigate, currentPage }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { isAuthenticated, logout } = useAuthStore();

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

    const handleNavClick = (page) => {
        onNavigate(page);
        setIsMenuOpen(false);
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand" onClick={() => handleNavClick('home')}>
                    <FiGithub size={32} />
                    <span>Bug Detection System</span>
                </div>

                <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
                    <a
                        className={currentPage === 'home' ? 'active' : ''}
                        onClick={() => handleNavClick('home')}
                    >
                        <FiHome /> Home
                    </a>
                    <a
                        className={currentPage === 'about' ? 'active' : ''}
                        onClick={() => handleNavClick('about')}
                    >
                        <FiInfo /> About
                    </a>

                    {isAuthenticated ? (
                        <>
                            <a
                                className={currentPage === 'dashboard' ? 'active' : ''}
                                onClick={() => handleNavClick('dashboard')}
                            >
                                <FiUser /> Dashboard
                            </a>
                            <button className="nav-btn logout-btn" onClick={logout}>
                                Logout
                            </button>
                        </>
                    ) : (
                        <button className="nav-btn login-btn" onClick={() => handleNavClick('login')}>
                            <FiLogIn /> Login
                        </button>
                    )}
                </div>

                <button className="hamburger" onClick={toggleMenu}>
                    {isMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
