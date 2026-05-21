import {
  FiTarget,
  FiUsers,
  FiAward,
  FiTrendingUp,
  FiCode,
  FiDatabase,
  FiCpu,
  FiGitBranch,
} from "react-icons/fi";
import "./About.css";
import photo1 from "../img/photo1.jpg";
import photo2 from "../img/photo2.jpg";

const About = () => {
  return (
    <div className="about-page">
      {/* Hero Section */}
      <section className="about-hero">
        <div className="about-hero-content">
          <h1>🐛 GitHub Bug Hunter</h1>
          <p className="about-subtitle">
            AI-Powered Bug Detection & Prediction System for GitHub Repositories
          </p>
          <p className="about-description">
            Leveraging Machine Learning, Google Gemini AI, and Advanced Code
            Analysis to predict and prevent bugs before they impact your users.
          </p>
        </div>
      </section>

      {/* What We Do Section */}
      <section className="features-overview">
        <h2>🎯 What We Do</h2>
        <p className="section-intro">
          GitHub Bug Hunter is an intelligent system that analyzes your GitHub
          repositories to identify files with high bug risk. By combining
          traditional machine learning with cutting-edge AI, we provide
          actionable insights to improve code quality and reduce technical debt.
        </p>
        <div className="features-grid">
          <div className="feature-item">
            <span className="feature-icon">🔍</span>
            <h3>Repository Analysis</h3>
            <p>
              Analyze any GitHub repository by URL, examining commit history,
              code changes, and issue patterns
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🤖</span>
            <h3>ML-Powered Predictions</h3>
            <p>
              Random Forest classifier trained on bug patterns to predict
              file-level risk scores (0-100%)
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">✨</span>
            <h3>Gemini AI Analysis</h3>
            <p>
              Google Gemini 2.5 Flash provides deep code insights, security
              vulnerability detection, and actionable recommendations
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🔐</span>
            <h3>Security Scanning</h3>
            <p>
              Detects 15+ types of security issues: SQL injection, XSS,
              hardcoded credentials, and more
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <h3>Real-Time Analytics</h3>
            <p>
              Track your analysis history, repository trends, and code quality
              metrics over time
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🎓</span>
            <h3>Self-Learning System</h3>
            <p>
              Incremental learning from user feedback to continuously improve
              prediction accuracy
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">👤</span>
            <h3>GitHub OAuth</h3>
            <p>
              Secure authentication to analyze private repositories and access
              your GitHub data
            </p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">💾</span>
            <h3>MongoDB Storage</h3>
            <p>
              Persistent storage of analysis results, user profiles, and
              historical data
            </p>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <h2>👥 Our Team</h2>
        <p className="section-intro">
          Dedicated to solving software development challenges through
          innovative AI solutions
        </p>
        <div className="team-grid">
          {/* <div className="team-member">
            <div className="member-avatar">👨‍🏫</div>
            <h3>Dr. Kaveri Umesh Kadam</h3>
            <p className="member-role">Team Mentor</p>
            <p className="member-bio">
              Guiding the project with expertise in software engineering and
              machine learning
            </p>
          </div> */}

          <div className="team-member">
            <div className="member-avatar">
  <img src={photo1} alt="Nadim Ahamad" />
</div> 
            <h3>Nadim Ahamad</h3>
            <p className="member-role"> Team Leader</p>
            <p className="member-bio">
              Contributing to backend development and frontend development and
              UI design
            </p>
          </div>
          <div className="team-member">
            <div className="member-avatar">
  <img src={photo2} alt="Mohd Sameem" />
</div>
            <h3>Mohd Sameem</h3>
            <p className="member-role">Team Member</p>
            <p className="member-bio">Working on ML model implementation</p>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="tech-stack-section">
        <h2>🛠️ Technology Stack</h2>
        <div className="tech-category">
          <h3>
            <FiCode /> Frontend
          </h3>
          <div className="tech-tags">
            <span className="tech-tag">React 18</span>
            <span className="tech-tag">Vite</span>
            <span className="tech-tag">React Router</span>
            <span className="tech-tag">React Icons</span>
            <span className="tech-tag">Chart.js</span>
            <span className="tech-tag">CSS3</span>
            <span className="tech-tag">JavaScript ES6+</span>
          </div>
        </div>
        <div className="tech-category">
          <h3>
            <FiDatabase /> Backend
          </h3>
          <div className="tech-tags">
            <span className="tech-tag">Python 3.11</span>
            <span className="tech-tag">FastAPI</span>
            <span className="tech-tag">Uvicorn</span>
            <span className="tech-tag">Pydantic</span>
            <span className="tech-tag">PyGithub</span>
            <span className="tech-tag">Python-dotenv</span>
          </div>
        </div>
        <div className="tech-category">
          <h3>
            <FiCpu /> Machine Learning & AI
          </h3>
          <div className="tech-tags">
            <span className="tech-tag">scikit-learn</span>
            <span className="tech-tag">Random Forest</span>
            <span className="tech-tag">Pandas</span>
            <span className="tech-tag">NumPy</span>
            <span className="tech-tag">Google Gemini AI</span>
            <span className="tech-tag">Joblib</span>
          </div>
        </div>
        <div className="tech-category">
          <h3>
            <FiDatabase /> Database & Storage
          </h3>
          <div className="tech-tags">
            <span className="tech-tag">MongoDB</span>
            <span className="tech-tag">PyMongo</span>
            <span className="tech-tag">Motor (Async)</span>
            <span className="tech-tag">JSON Storage</span>
          </div>
        </div>
        <div className="tech-category">
          <h3>
            <FiGitBranch /> Authentication & APIs
          </h3>
          <div className="tech-tags">
            <span className="tech-tag">GitHub OAuth</span>
            <span className="tech-tag">Authlib</span>
            <span className="tech-tag">JWT (python-jose)</span>
            <span className="tech-tag">HTTPX</span>
            <span className="tech-tag">GitHub REST API</span>
          </div>
        </div>
      </section>

      {/* ML Model Section */}
      <section className="ml-section">
        <h2>🧠 Machine Learning Architecture</h2>
        <div className="ml-content">
          <div className="ml-description">
            <h3>Random Forest Classifier</h3>
            <p>
              Our primary ML model uses <strong>Random Forest</strong>, an
              ensemble learning method that combines multiple decision trees to
              make accurate predictions. The model is trained on historical
              commit data, bug patterns, and code complexity metrics.
            </p>
            <h4>Key Features Analyzed:</h4>
            <ul>
              <li>
                <strong>Bug Keywords:</strong> Frequency of bug-related terms
                (fix, bug, error, hotfix, patch) in commit messages
              </li>
              <li>
                <strong>Lines Changed:</strong> Average number of lines modified
                per commit (complexity indicator)
              </li>
              <li>
                <strong>Commit Frequency:</strong> How often a file is modified
                (churn rate)
              </li>
              <li>
                <strong>Critical Issues:</strong> Count of critical security
                vulnerabilities detected
              </li>
              <li>
                <strong>High Issues:</strong> Count of high-severity code
                quality problems
              </li>
            </ul>
            <h4>Model Configuration:</h4>
            <ul>
              <li>Algorithm: Random Forest Classifier</li>
              <li>Estimators: 100 decision trees</li>
              <li>Random State: 42 (reproducibility)</li>
              <li>Warm Start: Enabled for incremental learning</li>
            </ul>
          </div>
          <div className="ml-workflow">
            <h3>🔄 Learning Workflow</h3>
            <div className="workflow-steps">
              <div className="workflow-step">
                <span className="step-number">1</span>
                <h4>Data Collection</h4>
                <p>Fetch commits, diffs, and issues from GitHub API</p>
              </div>
              <div className="workflow-step">
                <span className="step-number">2</span>
                <h4>Feature Extraction</h4>
                <p>Extract bug keywords, complexity metrics, and patterns</p>
              </div>
              <div className="workflow-step">
                <span className="step-number">3</span>
                <h4>Risk Prediction</h4>
                <p>ML model calculates 0-1 risk score for each file</p>
              </div>
              <div className="workflow-step">
                <span className="step-number">4</span>
                <h4>Gemini AI Analysis</h4>
                <p>Deep code analysis with security recommendations</p>
              </div>
              <div className="workflow-step">
                <span className="step-number">5</span>
                <h4>User Feedback</h4>
                <p>Collect feedback on prediction accuracy</p>
              </div>
              <div className="workflow-step">
                <span className="step-number">6</span>
                <h4>Incremental Learning</h4>
                <p>Retrain model with new feedback data</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Gemini AI Section */}
      <section className="gemini-section">
        <h2>✨ Google Gemini AI Integration</h2>
        <div className="gemini-content">
          <p className="gemini-intro">
            We leverage <strong>Google Gemini 2.5 Flash</strong>, a
            state-of-the-art large language model, to provide deep code analysis
            and intelligent recommendations that go beyond traditional static
            analysis.
          </p>
          <div className="gemini-features">
            <div className="gemini-feature">
              <h3>🔍 Deep Code Understanding</h3>
              <p>
                Gemini analyzes code semantics, logic flow, and architectural
                patterns to identify subtle bugs that rule-based systems miss
              </p>
            </div>
            <div className="gemini-feature">
              <h3>🛡️ Security Vulnerability Detection</h3>
              <p>
                Identifies SQL injection, XSS, CSRF, hardcoded credentials, and
                other OWASP Top 10 vulnerabilities with CVE references
              </p>
            </div>
            <div className="gemini-feature">
              <h3>💡 Actionable Recommendations</h3>
              <p>
                Provides step-by-step fix instructions, code examples, and best
                practice guidance for each issue found
              </p>
            </div>
            <div className="gemini-feature">
              <h3>📊 Comprehensive Reports</h3>
              <p>
                Generates detailed 400+ word analysis reports covering security
                posture, code quality, and maintenance concerns
              </p>
            </div>
          </div>
          <div className="gemini-capabilities">
            <h3>What Gemini Detects:</h3>
            <div className="capabilities-grid">
              <div className="capability">SQL Injection</div>
              <div className="capability">XSS Vulnerabilities</div>
              <div className="capability">Hardcoded Secrets</div>
              <div className="capability">Empty Catch Blocks</div>
              <div className="capability">Deprecated APIs</div>
              <div className="capability">Magic Numbers</div>
              <div className="capability">Code Smells</div>
              <div className="capability">Logic Errors</div>
              <div className="capability">Memory Leaks</div>
              <div className="capability">Race Conditions</div>
              <div className="capability">Null Pointer Issues</div>
              <div className="capability">Type Coercion Bugs</div>
            </div>
          </div>
        </div>
      </section>

      {/* Architecture Diagram Section */}
      <section className="architecture-section">
        <h2>🏗️ System Architecture</h2>
        <div className="architecture-diagram">
          <pre className="diagram-code">
            {`
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Dashboard  │  │  Repository  │  │   Analytics  │         │
│  │              │  │    List      │  │   Dashboard  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                    React + Vite Frontend                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                          │  │
│  │  /analyze-github-url  │  /auth/github  │  /user/stats   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌───────────────┬──────────┴──────────┬──────────────────┐   │
│  │               │                     │                   │   │
│  ▼               ▼                     ▼                   ▼   │
│ ┌─────────┐  ┌─────────┐  ┌──────────────┐  ┌──────────────┐ │
│ │ GitHub  │  │   ML    │  │    Gemini    │  │     User     │ │
│ │Analyzer │  │Predictor│  │   Analyzer   │  │   Manager    │ │
│ └─────────┘  └─────────┘  └──────────────┘  └──────────────┘ │
│      │            │              │                   │          │
└──────┼────────────┼──────────────┼───────────────────┼──────────┘
       │            │              │                   │
       ▼            ▼              ▼                   ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐
│  GitHub  │  │   ML     │  │  Gemini  │  │     MongoDB      │
│   API    │  │  Model   │  │ 2.5 Flash│  │   Database       │
│          │  │  (PKL)   │  │   API    │  │                  │
│  Commits │  │ Random   │  │          │  │  Users           │
│  Issues  │  │ Forest   │  │  Deep    │  │  Analyses        │
│  Diffs   │  │          │  │ Analysis │  │  Feedback        │
└──────────┘  └──────────┘  └──────────┘  └──────────────────┘

                    ┌──────────────────────┐
                    │  Incremental Learner │
                    │  (Self-Learning)     │
                    │  Feedback Loop       │
                    └──────────────────────┘
`}
          </pre>
        </div>
        <div className="architecture-description">
          <h3>Data Flow:</h3>
          <ol>
            <li>
              <strong>User Input:</strong> User provides GitHub repository URL
              through React frontend
            </li>
            <li>
              <strong>GitHub Analysis:</strong> Backend fetches commits, diffs,
              and issues via PyGithub
            </li>
            <li>
              <strong>Code Analysis:</strong> Static code analyzer detects
              security issues and code smells
            </li>
            <li>
              <strong>ML Prediction:</strong> Random Forest model calculates
              risk scores for each file
            </li>
            <li>
              <strong>Gemini AI:</strong> Deep analysis with Google Gemini for
              comprehensive insights
            </li>
            <li>
              <strong>Data Storage:</strong> Results saved to MongoDB with user
              profile
            </li>
            <li>
              <strong>Response:</strong> Combined results returned to frontend
              with visualizations
            </li>
            <li>
              <strong>Feedback Loop:</strong> User feedback collected for
              incremental learning
            </li>
          </ol>
        </div>
      </section>

      {/* Self-Learning Section */}
      <section className="learning-section">
        <h2>🎓 Self-Learning System</h2>
        <div className="learning-content">
          <p className="learning-intro">
            Our system implements <strong>Incremental Learning</strong>,
            allowing the ML model to continuously improve from user feedback
            without requiring complete retraining from scratch.
          </p>
          <div className="learning-features">
            <div className="learning-feature">
              <h3>📝 Feedback Collection</h3>
              <p>
                Users can mark predictions as accurate or inaccurate, providing
                ground truth labels for model improvement
              </p>
            </div>
            <div className="learning-feature">
              <h3>🔄 Automatic Retraining</h3>
              <p>
                When 20+ feedback items are collected, the system automatically
                retrains the model with new data
              </p>
            </div>
            <div className="learning-feature">
              <h3>📊 Performance Tracking</h3>
              <p>
                Learning statistics tracked: total analyses, feedback
                percentage, and model accuracy over time
              </p>
            </div>
            <div className="learning-feature">
              <h3>💾 History Persistence</h3>
              <p>
                All feedback and analysis history stored in JSON format for
                reproducibility and auditing
              </p>
            </div>
          </div>
          <div className="learning-algorithm">
            <h3>Learning Algorithm:</h3>
            <p>
              We use <strong>warm_start=True</strong> in Random Forest, enabling
              incremental updates without discarding previous knowledge. This
              approach combines the benefits of online learning with the
              robustness of ensemble methods.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="mission-content">
          <div className="mission-icon">
            <FiTarget size={48} />
          </div>
          <h2>Our Mission</h2>
          <p>
            To revolutionize software development by making bug detection
            intelligent, proactive, and accessible to every developer. We
            combine cutting-edge AI with practical software engineering to help
            teams ship better software faster, reducing technical debt and
            improving code quality across the industry.
          </p>
        </div>
      </section>

      {/* Values Section */}
      <section className="values-section">
        <h2>Our Core Values</h2>
        <div className="values-grid">
          <div className="value-card">
            <div className="value-icon">
              <FiAward />
            </div>
            <h3>Excellence</h3>
            <p>
              We strive for the highest quality in code analysis, prediction
              accuracy, and user experience
            </p>
          </div>
          <div className="value-card">
            <div className="value-icon">
              <FiUsers />
            </div>
            <h3>Community</h3>
            <p>
              We believe in open source, collaboration, and helping developers
              worldwide improve their code
            </p>
          </div>
          <div className="value-card">
            <div className="value-icon">
              <FiTrendingUp />
            </div>
            <h3>Innovation</h3>
            <p>
              We continuously push boundaries by integrating the latest AI and
              ML technologies
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
