import { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import { FiGithub } from 'react-icons/fi'
import useAuthStore from './store/authStore'
import LoginPage from './components/LoginPage'
import Dashboard from './components/Dashboard'
import BugPredictor from './components/BugPredictor'
import './App.css'

function App() {
    const { isAuthenticated, logout } = useAuthStore()
    const [showDashboard, setShowDashboard] = useState(() => {
        // Check if we should show dashboard on initial load
        const urlParams = new URLSearchParams(window.location.search)
        const hasOAuthCode = urlParams.get('code') !== null
        return hasOAuthCode // If OAuth code is present, we're returning from GitHub
    })

    // Check URL for classic mode parameter
    const urlParams = new URLSearchParams(window.location.search)
    const isClassicMode = urlParams.get('classic') === 'true'

    // Monitor authentication changes
    useEffect(() => {
        console.log('🔄 Auth state changed - isAuthenticated:', isAuthenticated)
        if (isAuthenticated) {
            // User just logged in, ensure we're showing the dashboard
            console.log('✅ User authenticated, clearing URL params')
            window.history.replaceState({}, document.title, '/')
        }
    }, [isAuthenticated])

    // Debug logging
    console.log('🔍 App render - isAuthenticated:', isAuthenticated, 'showDashboard:', showDashboard, 'isClassicMode:', isClassicMode, 'hasOAuthCode:', urlParams.get('code') !== null)

    const handleBackToClassic = () => {
        logout()
        setShowDashboard(false)
    }

    // If authenticated, always show dashboard view
    // If not authenticated and showDashboard is true, show login page
    // Otherwise show classic view

    if (isAuthenticated) {
        // User is logged in - show dashboard
        console.log('✅ Rendering Dashboard (user is authenticated)')
        return (
            <div className="App">
                <Dashboard />
                <button
                    onClick={handleBackToClassic}
                    style={{
                        position: 'fixed',
                        bottom: '1rem',
                        right: '1rem',
                        padding: '0.5rem 1rem',
                        background: '#21262d',
                        color: '#c9d1d9',
                        border: '1px solid #30363d',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        zIndex: 1000,
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem'
                    }}
                >
                    Logout & Classic View
                </button>
                <Toaster position="top-right" />
            </div>
        )
    }

    if (showDashboard && !isClassicMode) {
        // User clicked login button - show login page
        console.log('🔐 Rendering Login Page')
        return (
            <div className="App">
                <LoginPage onBack={() => {
                    setShowDashboard(false)
                    // Clear any URL params
                    window.history.replaceState({}, document.title, '/')
                }} />
                <Toaster position="top-right" />
            </div>
        )
    }

    // Default - show classic view
    console.log('🏠 Rendering Classic View (isClassicMode:', isClassicMode, ')')
    return (
        <div className="App">
            <header>
                <div className="header-content">
                    <div>
                        <h1>🐛 Github Bug Detection System</h1>
                        <p>Analyze GitHub repositories to detect and predict bugs</p>
                    </div>
                    <button
                        onClick={(e) => {
                            e.preventDefault()
                            console.log('🖱️ Login button clicked, setting showDashboard to true')
                            // Clear any URL params that might interfere
                            window.history.replaceState({}, document.title, '/')
                            setShowDashboard(true)
                        }}
                        className="login-btn"
                    >
                        <FiGithub size={20} />
                        Login for Dashboard
                    </button>
                </div>
            </header>
            <BugPredictor />
            <Toaster position="top-right" />
        </div>
    )
}

export default App
