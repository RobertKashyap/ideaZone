/**
 * IndexedDB Key Store - Using idb-keyval pattern
 * 
 * Stores user API keys and other sensitive data locally.
 * Uses IndexedDB for persistence across sessions.
 */

import { get, set, del, keys } from 'idb-keyval'

// ============ API Keys ============

export interface ApiKeys {
    geminiApiKey?: string
    googleSearchApiKey?: string
    googleSearchCx?: string
}

const API_KEYS_KEY = 'api_keys'

export async function getApiKeys(): Promise<ApiKeys> {
    const stored = await get<ApiKeys>(API_KEYS_KEY)
    return stored || {}
}

export async function setApiKeys(keys: ApiKeys): Promise<void> {
    await set(API_KEYS_KEY, keys)
}

export async function clearApiKeys(): Promise<void> {
    await del(API_KEYS_KEY)
}

// ============ Cached Ideas (for offline) ============

const IDEA_PREFIX = 'idea_'

export async function cacheIdea(id: string, idea: unknown): Promise<void> {
    await set(`${IDEA_PREFIX}${id}`, idea)
}

export async function getCachedIdea(id: string): Promise<unknown | null> {
    return get(`${IDEA_PREFIX}${id}`)
}

export async function getCachedIdeaIds(): Promise<string[]> {
    const allKeys = await keys()
    return allKeys
        .filter((k) => typeof k === 'string' && k.startsWith(IDEA_PREFIX))
        .map((k) => (k as string).replace(IDEA_PREFIX, ''))
}

export async function clearCachedIdea(id: string): Promise<void> {
    await del(`${IDEA_PREFIX}${id}`)
}

// ============ Draft Transcripts (for offline editing) ============

const DRAFT_PREFIX = 'draft_'

export async function saveDraft(ideaId: string, text: string): Promise<void> {
    await set(`${DRAFT_PREFIX}${ideaId}`, { text, savedAt: new Date().toISOString() })
}

export async function getDraft(ideaId: string): Promise<{ text: string; savedAt: string } | null> {
    return (await get<{ text: string; savedAt: string }>(`${DRAFT_PREFIX}${ideaId}`)) ?? null
}

export async function clearDraft(ideaId: string): Promise<void> {
    await del(`${DRAFT_PREFIX}${ideaId}`)
}
