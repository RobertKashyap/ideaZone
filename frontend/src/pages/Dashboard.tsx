import AudioRecorder from '../components/AudioRecorder'
import TranscriptionEditor from '../components/TranscriptionEditor'

/**
 * Dashboard Page - Placeholder
 * 
 * Future endpoints this page will call:
 * - GET /ideas - List all ideas
 * - POST /ideas - Create new idea
 */
function Dashboard() {
    return (
        <div className="container">
            <header style={{ marginBottom: '2rem' }}>
                <h1>💡 Idea Tracker</h1>
                <p className="text-secondary">
                    Record your ideas, get AI-powered transcription and research
                </p>
            </header>

            <section style={{ marginBottom: '2rem' }}>
                <h2>Quick Capture</h2>
                <AudioRecorder />
            </section>

            <section style={{ marginBottom: '2rem' }}>
                <h2>Recent Ideas</h2>
                <div className="placeholder">
                    <div className="placeholder-icon">📝</div>
                    <p>No ideas yet. Record your first idea above!</p>
                    <p className="text-secondary" style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                        Will call: <code>GET /ideas</code>
                    </p>
                </div>
            </section>

            <section>
                <h2>Transcription Preview</h2>
                <TranscriptionEditor />
            </section>
        </div>
    )
}

export default Dashboard
