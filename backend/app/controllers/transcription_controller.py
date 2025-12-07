"""Transcription Controller - orchestrates transcription workflow."""
from typing import Literal, Optional
from uuid import UUID

from sqlmodel import Session

from app.logger import logger
from app.models import IdeaStatus
from app.repos import idea_repo, transcript_repo
from app.services import audio_service, cleaning_service, transcription_service

AdapterType = Literal["gemini", "dummy"]


async def transcribe_and_clean(
    session: Session,
    idea_id: UUID,
    adapter_type: AdapterType = "dummy",
    api_key: Optional[str] = None
) -> dict:
    """Full transcription workflow: transcribe audio and clean text.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        Dict with raw and cleaned transcription
    """
    logger.info(f"Starting transcription workflow for idea {idea_id}")
    
    # Get idea and validate
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise ValueError(f"Idea not found: {idea_id}")
    
    if not idea.audio_blob:
        raise ValueError(f"No audio uploaded for idea: {idea_id}")
    
    # Transcribe audio
    raw_text = await transcription_service.transcribe_audio_bytes(
        audio_bytes=idea.audio_blob,
        adapter_type=adapter_type,
        api_key=api_key
    )
    
    # Clean transcript
    cleaned_text = cleaning_service.clean_transcript(raw_text)
    
    # Check if transcript exists
    existing = transcript_repo.get_transcript_by_idea(session, idea_id)
    
    if existing:
        # Update existing transcript
        transcript = transcript_repo.update_transcript(
            session,
            existing.id,
            raw_text=raw_text,
            cleaned_text=cleaned_text
        )
    else:
        # Create new transcript
        transcript = transcript_repo.create_transcript(
            session,
            idea_id=idea_id,
            raw_text=raw_text,
            cleaned_text=cleaned_text
        )
    
    # Update idea status
    idea_repo.update_idea_status(session, idea_id, IdeaStatus.TRANSCRIBED)
    
    logger.info(f"Transcription complete for idea {idea_id}")
    
    return {
        "transcript_id": str(transcript.id),
        "transcription_raw": raw_text,
        "transcription_clean": cleaned_text
    }
