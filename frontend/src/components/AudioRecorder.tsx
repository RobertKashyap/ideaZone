import { useState, useRef, useEffect, useCallback } from 'react'

interface AudioRecorderProps {
    ideaId?: string
    initialAudioUrl?: string | null
    onAudioUploaded?: (audioPath: string) => void
    onError?: (error: string) => void
}

/**
 * Audio Recorder Component
 * - Records audio from microphone using MediaRecorder API
 * - Shows visual waveform animation while recording
 * - Supports file upload as alternative
 * - Uploads to backend API
 */
function AudioRecorder({ ideaId, initialAudioUrl, onAudioUploaded, onError }: AudioRecorderProps) {
    const [isRecording, setIsRecording] = useState(false)
    const [isUploading, setIsUploading] = useState(false)
    const [recordingTime, setRecordingTime] = useState(0)
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
    const [audioUrl, setAudioUrl] = useState<string | null>(initialAudioUrl || null)
    const [uploadStatus, setUploadStatus] = useState<string | null>(null)

    useEffect(() => {
        if (initialAudioUrl) {
            setAudioUrl(initialAudioUrl)
        }
    }, [initialAudioUrl])

    const mediaRecorderRef = useRef<MediaRecorder | null>(null)
    const chunksRef = useRef<Blob[]>([])
    const timerRef = useRef<number | null>(null)
    const canvasRef = useRef<HTMLCanvasElement>(null)
    const analyserRef = useRef<AnalyserNode | null>(null)
    const animationRef = useRef<number | null>(null)

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (timerRef.current) clearInterval(timerRef.current)
            if (animationRef.current) cancelAnimationFrame(animationRef.current)
            if (audioUrl) URL.revokeObjectURL(audioUrl)
        }
    }, [audioUrl])

    // Draw waveform visualization
    const drawWaveform = useCallback(() => {
        if (!canvasRef.current || !analyserRef.current) return

        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        if (!ctx) return

        const analyser = analyserRef.current
        const bufferLength = analyser.frequencyBinCount
        const dataArray = new Uint8Array(bufferLength)

        const draw = () => {
            if (!isRecording) return
            animationRef.current = requestAnimationFrame(draw)

            analyser.getByteFrequencyData(dataArray)

            ctx.fillStyle = '#1e1e2e'
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            const barWidth = (canvas.width / bufferLength) * 2.5
            let x = 0

            for (let i = 0; i < bufferLength; i++) {
                const barHeight = (dataArray[i] / 255) * canvas.height * 0.8

                const gradient = ctx.createLinearGradient(0, canvas.height, 0, canvas.height - barHeight)
                gradient.addColorStop(0, '#6366f1')
                gradient.addColorStop(1, '#8b5cf6')
                ctx.fillStyle = gradient

                ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
                x += barWidth + 1
            }
        }

        draw()
    }, [isRecording])

    // Start recording
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

            // Setup audio analyzer for visualization
            const audioContext = new AudioContext()
            const source = audioContext.createMediaStreamSource(stream)
            const analyser = audioContext.createAnalyser()
            analyser.fftSize = 256
            source.connect(analyser)
            analyserRef.current = analyser

            const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
            mediaRecorderRef.current = mediaRecorder
            chunksRef.current = []

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data)
                }
            }

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
                setAudioBlob(blob)
                setAudioUrl(URL.createObjectURL(blob))
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorder.start(100)
            setIsRecording(true)
            setRecordingTime(0)
            setUploadStatus(null)

            timerRef.current = window.setInterval(() => {
                setRecordingTime(t => t + 1)
            }, 1000)

            drawWaveform()
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to access microphone'
            onError?.(message)
            setUploadStatus(`Error: ${message}`)
        }
    }

    // Stop recording
    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)
            if (timerRef.current) {
                clearInterval(timerRef.current)
                timerRef.current = null
            }
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current)
                animationRef.current = null
            }
        }
    }

    // Handle file upload input
    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            setAudioBlob(file)
            setAudioUrl(URL.createObjectURL(file))
            setUploadStatus(null)
        }
    }

    // Upload to backend
    const uploadAudio = async () => {
        if (!audioBlob || !ideaId) {
            setUploadStatus('Error: No audio or idea ID')
            return
        }

        setIsUploading(true)
        setUploadStatus('Uploading...')

        try {
            const formData = new FormData()
            formData.append('file', audioBlob, 'recording.webm')

            const response = await fetch(`http://localhost:8000/ideas/${ideaId}/audio`, {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`)
            }

            const data = await response.json()
            setUploadStatus(`✅ Uploaded! (${data.size_bytes} bytes)`)
            onAudioUploaded?.(data.audio_path)
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Upload failed'
            setUploadStatus(`❌ ${message}`)
            onError?.(message)
        } finally {
            setIsUploading(false)
        }
    }

    // Clear recording
    const clearRecording = () => {
        if (audioUrl) URL.revokeObjectURL(audioUrl)
        setAudioBlob(null)
        setAudioUrl(null)
        setRecordingTime(0)
        setUploadStatus(null)
    }

    // Delete audio from server
    const deleteAudioFromServer = async () => {
        if (!ideaId) return

        setIsUploading(true)
        setUploadStatus('Deleting from server...')

        try {
            const response = await fetch(`http://localhost:8000/ideas/${ideaId}/audio`, {
                method: 'DELETE',
            })

            if (!response.ok) {
                throw new Error(`Delete failed: ${response.status}`)
            }

            clearRecording()
            setUploadStatus('✅ Audio deleted from server')
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Delete failed'
            setUploadStatus(`❌ ${message}`)
            onError?.(message)
        } finally {
            setIsUploading(false)
        }
    }

    // Format time display
    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60)
        const secs = seconds % 60
        return `${mins}:${secs.toString().padStart(2, '0')}`
    }

    return (
        <div className="card">
            {/* Recording Controls */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
                <button
                    className="btn"
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isUploading}
                    style={{
                        background: isRecording
                            ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
                            : undefined
                    }}
                >
                    {isRecording ? '⏹️ Stop' : '🎙️ Record'}
                </button>

                <div className="text-secondary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    {isRecording ? (
                        <>
                            <span style={{
                                display: 'inline-block',
                                width: '10px',
                                height: '10px',
                                background: '#ef4444',
                                borderRadius: '50%',
                                animation: 'pulse 1s infinite'
                            }} />
                            <span style={{ color: '#ef4444', fontWeight: 'bold' }}>
                                Recording {formatTime(recordingTime)}
                            </span>
                        </>
                    ) : audioBlob ? (
                        <span style={{ color: '#22c55e' }}>✓ Audio ready ({formatTime(recordingTime)})</span>
                    ) : (
                        'Click to start recording'
                    )}
                </div>
            </div>

            {/* Waveform Visualization */}
            <div style={{
                marginTop: '1rem',
                borderRadius: '8px',
                overflow: 'hidden',
                background: '#1e1e2e',
                border: '1px solid var(--border)'
            }}>
                {isRecording ? (
                    <canvas
                        ref={canvasRef}
                        width={400}
                        height={80}
                        style={{ width: '100%', height: '80px' }}
                    />
                ) : audioUrl ? (
                    <audio
                        src={audioUrl}
                        controls
                        style={{ width: '100%', height: '60px' }}
                    />
                ) : (
                    <div style={{
                        height: '80px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--text-secondary)'
                    }}>
                        🎵 Audio preview will appear here
                    </div>
                )}
            </div>

            {/* File Upload Alternative */}
            <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                <label className="btn" style={{
                    background: 'var(--bg-dark)',
                    border: '1px solid var(--border)',
                    cursor: 'pointer'
                }}>
                    📁 Upload File
                    <input
                        type="file"
                        accept="audio/*"
                        onChange={handleFileUpload}
                        style={{ display: 'none' }}
                        disabled={isRecording || isUploading}
                    />
                </label>

                {audioBlob && (
                    <>
                        <button
                            className="btn"
                            onClick={uploadAudio}
                            disabled={isUploading || !ideaId}
                            style={{ background: ideaId ? undefined : 'gray' }}
                        >
                            {isUploading ? '⏳ Uploading...' : '☁️ Upload to Server'}
                        </button>
                        <button
                            className="btn"
                            onClick={clearRecording}
                            disabled={isUploading}
                            style={{ background: 'var(--bg-dark)', border: '1px solid var(--border)' }}
                        >
                            🗑️ Clear Local
                        </button>
                    </>
                )}

                {/* Delete from server button */}
                {ideaId && (
                    <button
                        className="btn"
                        onClick={deleteAudioFromServer}
                        disabled={isUploading}
                        style={{
                            background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100)',
                            marginLeft: audioBlob ? '0' : '0'
                        }}
                    >
                        🗑️ Delete from Server
                    </button>
                )}
            </div>

            {/* Status Message */}
            {uploadStatus && (
                <div style={{
                    marginTop: '1rem',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    background: uploadStatus.includes('✅') ? 'rgba(34, 197, 94, 0.1)' :
                        uploadStatus.includes('❌') ? 'rgba(239, 68, 68, 0.1)' :
                            'rgba(99, 102, 241, 0.1)',
                    color: uploadStatus.includes('✅') ? '#22c55e' :
                        uploadStatus.includes('❌') ? '#ef4444' :
                            'var(--primary)'
                }}>
                    {uploadStatus}
                </div>
            )}

            {!ideaId && (
                <p className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '1rem' }}>
                    ⚠️ Create an idea first to enable upload
                </p>
            )}

            <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
        </div>
    )
}

export default AudioRecorder
