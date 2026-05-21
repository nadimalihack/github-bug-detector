import { useEffect, useState } from 'react'
import { API_URL } from '../config'
import './ProgressModal.css'

const ProgressModal = ({ sessionId, onComplete, onError }) => {
    const [progress, setProgress] = useState(0)
    const [status, setStatus] = useState('starting')
    const [message, setMessage] = useState('Initializing analysis...')
    const [details, setDetails] = useState([])

    useEffect(() => {
        if (!sessionId) return

        const eventSource = new EventSource(`${API_URL}/progress/${sessionId}`)

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)

                if (data.type === 'keepalive') return

                setStatus(data.status)
                setMessage(data.message)

                if (data.progress !== undefined) {
                    setProgress(data.progress)
                }

                if (data.detail) {
                    setDetails(prev => [...prev, {
                        text: data.detail,
                        timestamp: data.timestamp
                    }])
                }

                if (data.status === 'complete') {
                    setTimeout(() => {
                        eventSource.close()
                        onComplete()
                    }, 1000)
                } else if (data.status === 'error') {
                    eventSource.close()
                    onError(data.message)
                }
            } catch (err) {
                console.error('Progress parse error:', err)
            }
        }

        eventSource.onerror = () => {
            eventSource.close()
            onError('Connection lost')
        }

        return () => eventSource.close()
    }, [sessionId, onComplete, onError])

    const getStatusIcon = () => {
        switch (status) {
            case 'starting': return '🚀'
            case 'fetching': return '📡'
            case 'analyzing': return '🔍'
            case 'predicting': return '🤖'
            case 'recording': return '💾'
            case 'complete': return '✅'
            case 'error': return '❌'
            default: return '⏳'
        }
    }

    return (
        <div className="progress-modal-overlay">
            <div className="progress-modal">
                <div className="progress-header">
                    <span className="progress-icon">{getStatusIcon()}</span>
                    <h2>Analyzing Repository</h2>
                </div>

                <div className="progress-content">
                    <div className="progress-message">{message}</div>

                    <div className="progress-bar-container">
                        <div
                            className="progress-bar-fill"
                            style={{ width: `${progress}%` }}
                        >
                            <span className="progress-percentage">{progress}%</span>
                        </div>
                    </div>

                    {details.length > 0 && (
                        <div className="progress-details">
                            <div className="details-header">Analysis Progress:</div>
                            <div className="details-list">
                                {details.slice(-5).map((detail, idx) => (
                                    <div key={idx} className="detail-item">
                                        <span className="detail-bullet">•</span>
                                        <span className="detail-text">{detail.text}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                <div className="progress-footer">
                    <div className="progress-spinner"></div>
                    <span>Please wait while we analyze the repository...</span>
                </div>
            </div>
        </div>
    )
}

export default ProgressModal
