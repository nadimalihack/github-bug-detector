import { FiGithub, FiZap, FiShield, FiTrendingUp, FiCode, FiCheckCircle } from 'react-icons/fi';
import './Home.css';

const Home = ({ onNavigate }) => {
    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <div className="hero-text">
                        <h1>
                            <span className="gradient-text">AI-Powered</span> Bug Detection
                        </h1>
                        <p className="hero-subtitle">
                            Detect, predict, and prevent bugs in your GitHub repositories with advanced machine learning
                        </p>
                        <div className="hero-buttons">
                            <button className="btn-primary" onClick={() => onNavigate('login')}>
                                <FiGithub /> Get Started
                            </button>
                            <button className="btn-secondary" onClick={() => onNavigate('about')}>
                                Learn More
                            </button>
                        </div>
                    </div>
                    <div className="hero-image">
                        <div className="code-preview">
                            <div className="code-header">
                                <span className="dot red"></span>
                                <span className="dot yellow"></span>
                                <span className="dot green"></span>
                            </div>
                            <div className="code-content">
                                <pre>
                                    {`// AI analyzing your code...
function detectBugs(code) {
  const analysis = ai.analyze(code);
  return {
    bugs: analysis.detected,
    severity: analysis.level,
    suggestions: analysis.fixes
  };
}`}
                                </pre>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <h2>Powerful Features</h2>
                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiZap />
                        </div>
                        <h3>Real-time Analysis</h3>
                        <p>Instant bug detection and analysis as you push code to your repositories</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiShield />
                        </div>
                        <h3>Predictive Intelligence</h3>
                        <p>ML models predict potential bugs before they become critical issues</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiTrendingUp />
                        </div>
                        <h3>Analytics Dashboard</h3>
                        <p>Comprehensive insights and trends about your code quality over time</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiCode />
                        </div>
                        <h3>Smart Recommendations</h3>
                        <p>AI-powered suggestions to fix bugs and improve code quality</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiGithub />
                        </div>
                        <h3>GitHub Integration</h3>
                        <p>Seamless integration with your GitHub repositories and workflow</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">
                            <FiCheckCircle />
                        </div>
                        <h3>Automated Testing</h3>
                        <p>Continuous monitoring and automated testing for all your projects</p>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section">
                <div className="stats-grid">
                    <div className="stat-card">
                        <h3>10K+</h3>
                        <p>Repositories Analyzed</p>
                    </div>
                    <div className="stat-card">
                        <h3>50K+</h3>
                        <p>Bugs Detected</p>
                    </div>
                    <div className="stat-card">
                        <h3>95%</h3>
                        <p>Accuracy Rate</p>
                    </div>
                    <div className="stat-card">
                        <h3>24/7</h3>
                        <p>Monitoring</p>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <h2>Ready to Improve Your Code Quality?</h2>
                <p>Start detecting bugs with AI-powered analysis today</p>
                <button className="btn-primary large" onClick={() => onNavigate('login')}>
                    <FiGithub /> Connect Your GitHub
                </button>
            </section>
        </div>
    );
};

export default Home;
