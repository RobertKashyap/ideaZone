import { useState, useEffect } from 'react'
import AudioRecorder from '../components/AudioRecorder'
import TranscriptionEditor from '../components/TranscriptionEditor'

interface Idea {
    id: string
    title: string | null
    status: string
    audio_path: string | null
    created_at: string
}

interface TranscriptionResult {
    transcript_id: string
    transcription_raw: string
    transcription_clean: string
}

/**
 * Dashboard Page
 * - Create new ideas
 * - Record/upload audio
 * - Step-by-step workflow: Record → Transcribe → Summarize → Approve
 */
function Dashboard() {
    const [ideas, setIdeas] = useState<Idea[]>([])
    const [currentIdea, setCurrentIdea] = useState<Idea | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const [transcription, setTranscription] = useState<TranscriptionResult | null>(null)
    const [summary, setSummary] = useState<{ bullets: string[], summary: string } | null>(null)
    const [tags, setTags] = useState<{ name: string, confidence: number }[]>([])
    const [workflowStep, setWorkflowStep] = useState<number>(0)
    const [statusMessage, setStatusMessage] = useState<string | null>(null)

    // Load ideas on mount
    useEffect(() => {
        loadIdeas()
    }, [])

    const loadIdeas = async () => {
        try {
            const res = await fetch('http://localhost:8000/ideas')
            if (res.ok) {
                const data = await res.json()
                setIdeas(data)
            }
        } catch (err) {
            console.error('Failed to load ideas:', err)
        }
    }

    // Create new idea
    const createNewIdea = async () => {
        setIsLoading(true)
        setStatusMessage('Creating new idea...')
        try {
            const res = await fetch('http://localhost:8000/ideas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            })
            if (res.ok) {
                const idea = await res.json()
                setCurrentIdea(idea)
                setIdeas([idea, ...ideas])
                setWorkflowStep(1)
                setTranscription(null)
                setSummary(null)
                setTags([])
                setStatusMessage(`✅ Idea created: ${idea.id.slice(0, 8)}...`)
            }
        } catch (err) {
            setStatusMessage('❌ Failed to create idea')
        } finally {
            setIsLoading(false)
        }
    }

    // Handle audio uploaded
    const handleAudioUploaded = (audioPath: string) => {
        if (currentIdea) {
            setCurrentIdea({ ...currentIdea, audio_path: audioPath })
            setWorkflowStep(2)
            setStatusMessage('✅ Audio uploaded! Ready to transcribe.')
        }
    }

    // Transcribe audio
    const handleTranscribe = async () => {
        if (!currentIdea) return
        setIsLoading(true)
        setStatusMessage('🔄 Transcribing audio...')
        try {
            const res = await fetch(`http://localhost:8000/ideas/${currentIdea.id}/transcribe`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ adapter: 'dummy' })
            })
            if (res.ok) {
                const data = await res.json()
                setTranscription(data)
                setWorkflowStep(3)
                setStatusMessage('✅ Transcription complete!')
            }
        } catch (err) {
            setStatusMessage('❌ Transcription failed')
        } finally {
            setIsLoading(false)
        }
    }

    // Generate summary
    const handleSummarize = async () => {
        if (!transcription) return
        setIsLoading(true)
        setStatusMessage('🔄 Generating summary...')
        try {
            // Get bullets
            const bulletsRes = await fetch('http://localhost:8000/summaries/bullets', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: transcription.transcription_clean, adapter: 'dummy' })
            })

            // Get tags
            const tagsRes = await fetch('http://localhost:8000/tags/suggest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: transcription.transcription_clean, adapter: 'dummy' })
            })

            if (bulletsRes.ok && tagsRes.ok) {
                const bulletsData = await bulletsRes.json()
                const tagsData = await tagsRes.json()
                setSummary({ bullets: bulletsData.bullets, summary: '' })
                setTags(tagsData.tags)
                setWorkflowStep(4)
                setStatusMessage('✅ Summary generated!')
            }
        } catch (err) {
            setStatusMessage('❌ Summary generation failed')
        } finally {
            setIsLoading(false)
        }
    }

    // Approve idea
    const handleApprove = async () => {
        if (!currentIdea) return
        setIsLoading(true)
        setStatusMessage('🔄 Approving idea...')
        try {
            const res = await fetch(`http://localhost:8000/ideas/${currentIdea.id}/approve`, {
                method: 'POST'
            })
            if (res.ok) {
                const data = await res.json()
                setCurrentIdea({ ...currentIdea, status: data.status })
                setWorkflowStep(5)
                setStatusMessage('✅ Idea approved for research!')
                loadIdeas()
            }
        } catch (err) {
            setStatusMessage('❌ Approval failed')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="container">
            <header style={{ marginBottom: '2rem' }}>
                <h1>💡 Idea Tracker</h1>
                <p className="text-secondary">
                    Record your ideas, get AI-powered transcription and research
                </p>
            </header>

            {/* Status Message */}
            {statusMessage && (
                <div style={{
                    padding: '1rem',
                    marginBottom: '1.5rem',
                    borderRadius: '8px',
                    background: statusMessage.includes('✅') ? 'rgba(34, 197, 94, 0.1)' :
                        statusMessage.includes('❌') ? 'rgba(239, 68, 68, 0.1)' :
                            'rgba(99, 102, 241, 0.1)',
                    border: `1px solid ${statusMessage.includes('✅') ? '#22c55e' :
                        statusMessage.includes('❌') ? '#ef4444' :
                            'var(--primary)'}`,
                    color: statusMessage.includes('✅') ? '#22c55e' :
                        statusMessage.includes('❌') ? '#ef4444' :
                            'var(--primary)'
                }}>
                    {statusMessage}
                </div>
            )}

            {/* Workflow Progress */}
            <div style={{
                display: 'flex',
                gap: '0.5rem',
                marginBottom: '2rem',
                flexWrap: 'wrap'
            }}>
                {['Create', 'Record', 'Transcribe', 'Summarize', 'Approve'].map((step, i) => (
                    <div
                        key={step}
                        style={{
                            padding: '0.5rem 1rem',
                            borderRadius: '20px',
                            background: workflowStep > i ? 'var(--primary)' :
                                workflowStep === i ? 'rgba(99, 102, 241, 0.2)' :
                                    'var(--bg-card)',
                            color: workflowStep > i ? 'white' :
                                workflowStep === i ? 'var(--primary)' :
                                    'var(--text-secondary)',
                            border: workflowStep === i ? '2px solid var(--primary)' : '1px solid var(--border)',
                            fontWeight: workflowStep >= i ? 600 : 400,
                            fontSize: '0.9rem'
                        }}
                    >
                        {workflowStep > i ? '✓ ' : ''}{step}
                    </div>
                ))}
            </div>

            {/* Step 1: Create Idea */}
            <section style={{ marginBottom: '2rem' }}>
                <h2>📝 Step 1: Create Idea</h2>
                <div className="card">
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
                        <button
                            className="btn"
                            onClick={createNewIdea}
                            disabled={isLoading}
                        >
                            {isLoading ? '⏳ Creating...' : '➕ New Idea'}
                        </button>
                        {currentIdea && (
                            <span className="badge" style={{ fontSize: '0.9rem' }}>
                                Current: {currentIdea.id.slice(0, 8)}... ({currentIdea.status})
                            </span>
                        )}
                    </div>
                </div>
            </section>

            {/* Step 2: Record Audio */}
            <section style={{ marginBottom: '2rem', opacity: workflowStep >= 1 ? 1 : 0.5 }}>
                <h2>🎙️ Step 2: Record Audio</h2>
                <AudioRecorder
                    ideaId={currentIdea?.id}
                    initialAudioUrl={currentIdea?.audio_path ? `http://localhost:8000/ideas/${currentIdea.id}/audio/download` : null}
                    onAudioUploaded={handleAudioUploaded}
                    onError={(err) => setStatusMessage(`❌ ${err}`)}
                />
            </section>

            {/* Step 3: Transcribe */}
            <section style={{ marginBottom: '2rem', opacity: workflowStep >= 2 ? 1 : 0.5 }}>
                <h2>📝 Step 3: Transcribe</h2>
                <div className="card">
                    <button
                        className="btn"
                        onClick={handleTranscribe}
                        disabled={isLoading || workflowStep < 2}
                    >
                        {isLoading ? '⏳ Transcribing...' : '🎯 Transcribe Audio'}
                    </button>

                    {transcription && (
                        <div style={{ marginTop: '1rem' }}>
                            <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Raw Transcript:</h3>
                            <div style={{
                                padding: '1rem',
                                background: 'var(--bg-dark)',
                                borderRadius: '8px',
                                border: '1px solid var(--border)',
                                maxHeight: '150px',
                                overflow: 'auto'
                            }}>
                                {transcription.transcription_raw}
                            </div>
                            <h3 style={{ fontSize: '1rem', marginTop: '1rem', marginBottom: '0.5rem' }}>Cleaned:</h3>
                            <TranscriptionEditor
                                initialText={transcription.transcription_clean}
                                transcriptId={transcription.transcript_id}
                            />
                        </div>
                    )}
                </div>
            </section>

            {/* Step 4: Summarize & Tag */}
            <section style={{ marginBottom: '2rem', opacity: workflowStep >= 3 ? 1 : 0.5 }}>
                <h2>✨ Step 4: Summarize & Tag</h2>
                <div className="card">
                    <button
                        className="btn"
                        onClick={handleSummarize}
                        disabled={isLoading || workflowStep < 3}
                    >
                        {isLoading ? '⏳ Generating...' : '🔮 Generate Summary & Tags'}
                    </button>

                    {summary && (
                        <div style={{ marginTop: '1rem' }}>
                            <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Key Points:</h3>
                            <ul style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
                                {summary.bullets.map((bullet, i) => (
                                    <li key={i} style={{ marginBottom: '0.5rem' }}>{bullet}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {tags.length > 0 && (
                        <div style={{ marginTop: '1rem' }}>
                            <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Suggested Tags:</h3>
                            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                {tags.map((tag, i) => (
                                    <span
                                        key={i}
                                        className="badge"
                                        style={{
                                            background: `rgba(99, 102, 241, ${tag.confidence})`,
                                        }}
                                    >
                                        {tag.name} ({Math.round(tag.confidence * 100)}%)
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </section>

            {/* Step 5: Approve */}
            <section style={{ marginBottom: '2rem', opacity: workflowStep >= 4 ? 1 : 0.5 }}>
                <h2>✅ Step 5: Approve for Research</h2>
                <div className="card">
                    <button
                        className="btn"
                        onClick={handleApprove}
                        disabled={isLoading || workflowStep < 4}
                        style={{
                            background: workflowStep >= 4 ? 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)' : undefined
                        }}
                    >
                        {isLoading ? '⏳ Approving...' : '🚀 Approve & Start Research'}
                    </button>

                    {workflowStep >= 5 && (
                        <div style={{
                            marginTop: '1rem',
                            padding: '1rem',
                            background: 'rgba(34, 197, 94, 0.1)',
                            borderRadius: '8px',
                            border: '1px solid #22c55e',
                            color: '#22c55e'
                        }}>
                            🎉 Idea approved! Research will begin soon. (Phase 2 feature)
                        </div>
                    )}
                </div>
            </section>

            {/* Recent Ideas */}
            <section>
                <h2>📚 Recent Ideas</h2>
                {ideas.length === 0 ? (
                    <div className="placeholder">
                        <div className="placeholder-icon">📝</div>
                        <p>No ideas yet. Create your first idea above!</p>
                    </div>
                ) : (
                    <div style={{ display: 'grid', gap: '1rem' }}>
                        {ideas.slice(0, 5).map(idea => (
                            <div
                                key={idea.id}
                                className="card"
                                style={{
                                    cursor: 'pointer',
                                    border: currentIdea?.id === idea.id ? '2px solid var(--primary)' : undefined
                                }}
                                onClick={() => {
                                    setCurrentIdea(idea)
                                    setWorkflowStep(idea.audio_path ? 2 : 1)
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <span style={{ fontFamily: 'monospace' }}>{idea.id.slice(0, 8)}...</span>
                                    <span className="badge">{idea.status}</span>
                                </div>
                                <div className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                                    {new Date(idea.created_at).toLocaleString()}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>
        </div>
    )
}

export default Dashboard
