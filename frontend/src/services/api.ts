/**
 * API Service - Central fetch wrapper
 * 
 * All backend API calls go through this service.
 * Base URL configured for local development.
 */

const API_BASE_URL = 'http://localhost:8000'

interface ApiResponse<T> {
    data?: T
    error?: string
}

/**
 * Generic fetch wrapper with error handling
 */
async function request<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<ApiResponse<T>> {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        })

        if (!response.ok) {
            const error = await response.text()
            return { error: error || `HTTP ${response.status}` }
        }

        const data = await response.json()
        return { data }
    } catch (err) {
        return { error: err instanceof Error ? err.message : 'Unknown error' }
    }
}

// ============ Health Check ============

export async function checkHealth(): Promise<ApiResponse<{ status: string }>> {
    return request<{ status: string }>('/health')
}

// ============ Ideas (stubs) ============

export async function getIdeas(): Promise<ApiResponse<unknown[]>> {
    // TODO: Implement when backend ready
    return request('/ideas')
}

export async function getIdea(id: string): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request(`/ideas/${id}`)
}

export async function createIdea(): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request('/ideas', { method: 'POST' })
}

// ============ Audio (stubs) ============

export async function uploadAudio(
    ideaId: string,
    audioBlob: Blob
): Promise<ApiResponse<unknown>> {
    // TODO: Implement multipart upload
    const formData = new FormData()
    formData.append('file', audioBlob)

    return fetch(`${API_BASE_URL}/ideas/${ideaId}/audio`, {
        method: 'POST',
        body: formData,
    }).then(async (res) => {
        if (!res.ok) return { error: `HTTP ${res.status}` }
        return { data: await res.json() }
    }).catch((err) => ({ error: err.message }))
}

// ============ Transcription (stubs) ============

export async function transcribeIdea(ideaId: string): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request(`/ideas/${ideaId}/transcribe`, { method: 'POST' })
}

export async function updateTranscript(
    transcriptId: string,
    text: string
): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request(`/transcripts/${transcriptId}`, {
        method: 'PUT',
        body: JSON.stringify({ text }),
    })
}

// ============ Research (stubs) ============

export async function approveIdea(ideaId: string): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request(`/ideas/${ideaId}/approve`, { method: 'POST' })
}

export async function getResearchReport(ideaId: string): Promise<ApiResponse<unknown>> {
    // TODO: Implement when backend ready
    return request(`/research/${ideaId}`)
}
