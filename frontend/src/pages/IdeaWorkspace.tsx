import { useParams } from 'react-router-dom'
import AudioRecorder from '../components/AudioRecorder'
import TranscriptionEditor from '../components/TranscriptionEditor'

/**
 * Idea Workspace Page - Placeholder
 * 
 * Future endpoints this page will call:
 * - GET /ideas/:id - Get idea details
 * - POST /ideas/:id/transcribe - Transcribe audio
 * - PUT /transcripts/:id - Save transcript edits
 * - POST /ideas/:id/approve - Approve idea for research
 * - GET /research/:id - Get research report
 */
function IdeaWorkspace() {
    const { id } = useParams<{ id: string }>()

    return (
        <div className="container">
            <header style={{ marginBottom: '2rem' }}>
                <a href="/" style={{ color: 'var(--primary)', textDecoration: 'none', marginBottom: '1rem', display: 'block' }}>
                    ← Back to Dashboard
                </a>
                <h1>Idea Workspace</h1>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <span className="badge">ID: {id || 'new'}</span>
                    <span className="badge">Status: Draft</span>
                </div>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                <section>
                    <h2>🎙️ Audio</h2>
                    <AudioRecorder />

                    <div style={{ marginTop: '1rem' }}>
                        <button className="btn">
                            📝 Transcribe
                        </button>
                        <p className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                            Will call: <code>POST /ideas/{id}/transcribe</code>
                        </p>
                    </div>
                </section>

                <section>
                    <h2>✏️ Transcript</h2>
                    <TranscriptionEditor />

                    <div style={{ marginTop: '1rem' }}>
                        <button className="btn">
                            ✅ Approve & Research
                        </button>
                        <p className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                            Will call: <code>POST /ideas/{id}/approve</code>
                        </p>
                    </div>
                </section>
            </div>

            <section style={{ marginTop: '2rem' }}>
                <h2>🔬 Research Report</h2>
                <div className="placeholder">
                    <div className="placeholder-icon">📊</div>
                    <p>Research report will appear here after approval</p>
                    <p className="text-secondary" style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                        Will poll: <code>GET /research/{id}</code>
                    </p>
                </div>
            </section>
        </div>
    )
}

export default IdeaWorkspace
