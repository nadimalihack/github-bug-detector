import { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import useAuthStore from './store/authStore'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import About from './pages/About'
import LoginPage from './components/LoginPage'
import Dashboard from './components/Dashboard'
import ClassicEvaluator from './components/ClassicEvaluator'
import './App.css'

function App() {
    const { isAuthenticated, logout, _hasHydrated } = useAuthStore()
    const [currentPage, setCurrentPage] = useState('home')
    const [showClassicView, setShowClassicView] = useState(false)

    // Initial page setup - check URL and authentication status
    useEffect(() => {
        // Wait for Zustand to hydrate from localStorage
        if (!_hasHydrated) {
            console.log('⏳ Waiting for store hydration...');
            return;
        }

        const urlParams = new URLSearchParams(window.location.search)
        const hasOAuthCode = urlParams.get('code') !== null
        const isClassicMode = urlParams.get('classic') === 'true'

        console.log('🔍 Initial check - OAuth code:', hasOAuthCode, 'Authenticated:', isAuthenticated, 'Classic:', isClassicMode, 'Hydrated:', _hasHydrated)

        if (isClassicMode) {
            setShowClassicView(true)
            setCurrentPage('classic')
        } else if (isAuthenticated) {
            // User is already authenticated, go to dashboard
            console.log('✅ User already authenticated, showing dashboard')
            setCurrentPage('dashboard')
        } else if (hasOAuthCode) {
            // OAuth callback in progress, show login page to process it
            console.log('🔑 OAuth code detected in URL, showing login page to process')
            setCurrentPage('login')
        }
    }, [isAuthenticated, _hasHydrated])

    // Monitor authentication changes - navigate to dashboard when user logs in
    useEffect(() => {
        if (isAuthenticated && !showClassicView) {
            console.log('✅ Authentication detected, navigating to dashboard')
            setCurrentPage('dashboard')
            // Clean up URL if there's an OAuth code
            const urlParams = new URLSearchParams(window.location.search)
            if (urlParams.get('code')) {
                window.history.replaceState({}, document.title, '/')
            }
        }
    }, [isAuthenticated, showClassicView])

    const handleNavigate = (page) => {
        setCurrentPage(page)
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const handleLogout = () => {
        logout()
        setCurrentPage('home')
    }

    const renderPage = () => {
        switch (currentPage) {
            case 'home':
                return <Home onNavigate={handleNavigate} />
            case 'about':
                return <About />
            case 'login':
                return <LoginPage onBack={() => handleNavigate('home')} onClassicView={() => {
                    setShowClassicView(true)
                    setCurrentPage('classic')
                }} />
            case 'dashboard':
                return isAuthenticated ? <Dashboard onClassicView={() => {
                    setShowClassicView(true)
                    setCurrentPage('classic')
                }} /> : <LoginPage onBack={() => handleNavigate('home')} onClassicView={() => {
                    setShowClassicView(true)
                    setCurrentPage('classic')
                }} />
            case 'classic':
                return <ClassicEvaluator onBackToDashboard={() => {
                    setShowClassicView(false)
                    if (isAuthenticated) {
                        setCurrentPage('dashboard')
                    } else {
                        setCurrentPage('home')
                    }
                }} />
            default:
                return <Home onNavigate={handleNavigate} />
        }
    }

    return (
        <div className="App">
            <Navbar
                onNavigate={handleNavigate}
                currentPage={currentPage}
            />
            <main style={{ minHeight: 'calc(100vh - 200px)' }}>
                {renderPage()}
            </main>
            <Footer />
            <Toaster position="top-right" />
        </div>
    )
}

export default App
