import { useState } from 'react'

/**
 * Transcription Editor Component - Placeholder
 * 
 * Future functionality:
 * - Display raw and cleaned transcription
 * - Allow editing of transcript
 * - Save edits to PUT /transcripts/:id
 */
function TranscriptionEditor() {
    const [transcript, setTranscript] = useState('')

    return (
        <div className="card">
            <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                    Transcript
                </label>
                <textarea
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                    placeholder="Transcription will appear here after recording and processing..."
                    style={{
                        width: '100%',
                        minHeight: '150px',
                        padding: '1rem',
                        background: 'var(--bg-dark)',
                        border: '1px solid var(--border)',
                        borderRadius: '8px',
                        color: 'var(--text-primary)',
                        fontSize: '1rem',
                        resize: 'vertical',
                    }}
                />
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button className="btn" style={{ background: 'var(--bg-dark)', border: '1px solid var(--border)' }}>
                    💾 Save
                </button>
                <button className="btn" style={{ background: 'var(--bg-dark)', border: '1px solid var(--border)' }}>
                    🔄 Regenerate
                </button>
            </div>

            <p className="text-secondary" style={{ fontSize: '0.85rem', marginTop: '1rem' }}>
                Will save to: <code>PUT /transcripts/:id</code>
            </p>
        </div>
    )
}

export default TranscriptionEditor
