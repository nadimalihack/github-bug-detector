import { FiGithub, FiMail, FiHeart, FiCode } from 'react-icons/fi';
import './Footer.css';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-content">
                    <div className="footer-section">
                        <h3><FiGithub /> Bug Detection System</h3>
                        <p>Advanced AI-powered bug detection and prediction for GitHub repositories.</p>
                    </div>

                    <div className="footer-section">
                        <h4>Quick Links</h4>
                        <ul>
                            <li><a href="#home">Home</a></li>
                            <li><a href="#about">About</a></li>
                            <li><a href="#features">Features</a></li>
                            <li><a href="#contact">Contact</a></li>
                        </ul>
                    </div>

                    <div className="footer-section">
                        <h4>Resources</h4>
                        <ul>
                            <li><a href="#docs">Documentation</a></li>
                            <li><a href="#api">API Reference</a></li>
                            <li><a href="#support">Support</a></li>
                            <li><a href="#privacy">Privacy Policy</a></li>
                        </ul>
                    </div>

                    <div className="footer-section">
                        <h4>Connect</h4>
                        <div className="social-links">
                            <a href="https://github.com/nadimalihack" target="_blank" rel="noopener noreferrer">
                                <FiGithub size={24} />
                            </a>
                            <a href="mailto:nadimalihack9289@gmail.com">
                                <FiMail size={24} />
                            </a>
                            <a href="#code">
                                <FiCode size={24} />
                            </a>
                        </div>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>
                        Made with <FiHeart className="heart-icon" /> by Bug Detection Team
                    </p>
                    <p>&copy; {currentYear} Bug Detection System. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
