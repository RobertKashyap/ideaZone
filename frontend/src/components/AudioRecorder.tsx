import { useState } from 'react'

/**
 * Audio Recorder Component - Placeholder
 * 
 * Future functionality:
 * - Record audio from microphone
 * - Upload recorded audio to POST /ideas/:id/audio
 * - Show recording status and waveform
 */
function AudioRecorder() {
    const [isRecording, setIsRecording] = useState(false)

    const handleRecordClick = () => {
        setIsRecording(!isRecording)
        // TODO: Implement actual recording with MediaRecorder API
        console.log(isRecording ? 'Stop recording' : 'Start recording')
    }

    return (
        <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <button
                    className="btn"
                    onClick={handleRecordClick}
                    style={{
                        background: isRecording
                            ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
                            : undefined
                    }}
                >
                    {isRecording ? '⏹️ Stop' : '🎙️ Record'}
                </button>

                <div className="text-secondary">
                    {isRecording ? (
                        <span style={{ color: '#ef4444' }}>● Recording...</span>
                    ) : (
                        'Click to start recording'
                    )}
                </div>
            </div>

            <div className="placeholder" style={{ marginTop: '1rem', padding: '1.5rem' }}>
                <div className="placeholder-icon">🎵</div>
                <p>Audio waveform visualization</p>
                <p className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    Will upload to: <code>POST /ideas/:id/audio</code>
                </p>
            </div>
        </div>
    )
}

export default AudioRecorder
