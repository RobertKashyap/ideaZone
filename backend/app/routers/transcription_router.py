"""Transcription Router - transcription endpoints."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.controllers import transcription_controller
from app.db import get_session
from app.repos import idea_repo, transcript_repo

router = APIRouter(prefix="/ideas", tags=["transcription"])


class TranscribeRequest(BaseModel):
    adapter: str = "dummy"
    api_key: Optional[str] = None


class TranscriptResponse(BaseModel):
    transcript_id: str
    transcription_raw: str
    transcription_clean: str


class TranscriptUpdateRequest(BaseModel):
    text: str


@router.post("/{idea_id}/transcribe", response_model=TranscriptResponse)
async def transcribe_idea(
    idea_id: UUID,
    data: TranscribeRequest = None,
    session: Session = Depends(get_session)
):
    """Transcribe audio for an idea.
    
    Uses the dummy adapter by default. Set adapter="gemini" and provide
    api_key to use Gemini for real transcription.
    """
    adapter = data.adapter if data else "dummy"
    api_key = data.api_key if data else None
    
    try:
        result = await transcription_controller.transcribe_and_clean(
            session, idea_id, adapter, api_key
        )
        return TranscriptResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{idea_id}/transcript")
async def get_transcript(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Get transcript for an idea."""
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    transcript = transcript_repo.get_transcript_by_idea(session, idea_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="No transcript found")
    
    return {
        "transcript_id": str(transcript.id),
        "idea_id": str(idea_id),
        "raw_text": transcript.raw_text,
        "cleaned_text": transcript.cleaned_text,
        "created_at": transcript.created_at.isoformat()
    }


@router.put("/transcripts/{transcript_id}")
async def update_transcript(
    transcript_id: UUID,
    data: TranscriptUpdateRequest,
    session: Session = Depends(get_session)
):
    """Update transcript text (for manual edits)."""
    transcript = transcript_repo.update_transcript(
        session, transcript_id, cleaned_text=data.text
    )
    
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    return {
        "transcript_id": str(transcript.id),
        "cleaned_text": transcript.cleaned_text,
        "updated": True
    }
