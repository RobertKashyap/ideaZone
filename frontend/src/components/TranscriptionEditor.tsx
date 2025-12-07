import { useState, useEffect } from 'react'

interface TranscriptionEditorProps {
    initialText?: string
    transcriptId?: string
    onSave?: (text: string) => void
}

/**
 * Transcription Editor Component
 * - Display and edit transcription text
 * - Save edits to backend
 */
function TranscriptionEditor({ initialText = '', transcriptId, onSave }: TranscriptionEditorProps) {
    const [text, setText] = useState(initialText)
    const [isSaving, setIsSaving] = useState(false)
    const [saveStatus, setSaveStatus] = useState<string | null>(null)
    const [isEdited, setIsEdited] = useState(false)

    useEffect(() => {
        setText(initialText)
        setIsEdited(false)
    }, [initialText])

    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(e.target.value)
        setIsEdited(true)
        setSaveStatus(null)
    }

    const handleSave = async () => {
        if (!transcriptId) {
            setSaveStatus('❌ No transcript ID')
            return
        }

        setIsSaving(true)
        setSaveStatus('Saving...')

        try {
            const res = await fetch(`http://localhost:8000/transcripts/${transcriptId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            })

            if (res.ok) {
                setSaveStatus('✅ Saved!')
                setIsEdited(false)
                onSave?.(text)
            } else {
                throw new Error(`Save failed: ${res.status}`)
            }
        } catch (err) {
            setSaveStatus('❌ Save failed')
        } finally {
            setIsSaving(false)
        }
    }

    const handleRevert = () => {
        setText(initialText)
        setIsEdited(false)
        setSaveStatus(null)
    }

    return (
        <div>
            <div style={{ marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label style={{ fontWeight: 500, fontSize: '0.9rem' }}>
                    Editable Transcript
                    {isEdited && <span style={{ color: 'var(--primary)', marginLeft: '0.5rem' }}>(modified)</span>}
                </label>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    {text.length} characters
                </span>
            </div>

            <textarea
                value={text}
                onChange={handleTextChange}
                placeholder="Transcription will appear here..."
                style={{
                    width: '100%',
                    minHeight: '120px',
                    padding: '1rem',
                    background: 'var(--bg-dark)',
                    border: isEdited ? '2px solid var(--primary)' : '1px solid var(--border)',
                    borderRadius: '8px',
                    color: 'var(--text-primary)',
                    fontSize: '0.95rem',
                    lineHeight: '1.6',
                    resize: 'vertical',
                    fontFamily: 'inherit'
                }}
            />

            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', flexWrap: 'wrap', alignItems: 'center' }}>
                <button
                    className="btn"
                    onClick={handleSave}
                    disabled={isSaving || !isEdited}
                    style={{
                        opacity: isEdited ? 1 : 0.5,
                        background: isEdited ? undefined : 'var(--bg-dark)',
                        border: isEdited ? undefined : '1px solid var(--border)'
                    }}
                >
                    {isSaving ? '⏳ Saving...' : '💾 Save Changes'}
                </button>

                {isEdited && (
                    <button
                        className="btn"
                        onClick={handleRevert}
                        style={{ background: 'var(--bg-dark)', border: '1px solid var(--border)' }}
                    >
                        ↩️ Revert
                    </button>
                )}

                {saveStatus && (
                    <span style={{
                        fontSize: '0.9rem',
                        color: saveStatus.includes('✅') ? '#22c55e' :
                            saveStatus.includes('❌') ? '#ef4444' :
                                'var(--primary)'
                    }}>
                        {saveStatus}
                    </span>
                )}
            </div>
        </div>
    )
}

export default TranscriptionEditor
