"""Transcript Repository - CRUD operations for transcripts."""
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import Transcript


def create_transcript(
    session: Session,
    idea_id: UUID,
    raw_text: str = "",
    cleaned_text: str = ""
) -> Transcript:
    """Create a new transcript.
    
    Args:
        session: Database session
        idea_id: Associated idea UUID
        raw_text: Raw transcription text
        cleaned_text: Cleaned transcription text
        
    Returns:
        Created transcript
    """
    transcript = Transcript(
        idea_id=idea_id,
        raw_text=raw_text,
        cleaned_text=cleaned_text
    )
    session.add(transcript)
    session.commit()
    session.refresh(transcript)
    return transcript


def get_transcript(session: Session, transcript_id: UUID) -> Optional[Transcript]:
    """Get a transcript by ID.
    
    Args:
        session: Database session
        transcript_id: Transcript UUID
        
    Returns:
        Transcript if found
    """
    return session.get(Transcript, transcript_id)


def get_transcript_by_idea(session: Session, idea_id: UUID) -> Optional[Transcript]:
    """Get transcript for an idea.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        
    Returns:
        Transcript if found
    """
    statement = select(Transcript).where(Transcript.idea_id == idea_id)
    results = session.exec(statement)
    return results.first()


def update_transcript(
    session: Session,
    transcript_id: UUID,
    raw_text: Optional[str] = None,
    cleaned_text: Optional[str] = None
) -> Optional[Transcript]:
    """Update a transcript.
    
    Args:
        session: Database session
        transcript_id: Transcript UUID
        raw_text: New raw text (optional)
        cleaned_text: New cleaned text (optional)
        
    Returns:
        Updated transcript if found
    """
    transcript = get_transcript(session, transcript_id)
    if transcript:
        if raw_text is not None:
            transcript.raw_text = raw_text
        if cleaned_text is not None:
            transcript.cleaned_text = cleaned_text
        session.add(transcript)
        session.commit()
        session.refresh(transcript)
    return transcript


def delete_transcript(session: Session, transcript_id: UUID) -> bool:
    """Delete a transcript.
    
    Args:
        session: Database session
        transcript_id: Transcript UUID
        
    Returns:
        True if deleted
    """
    transcript = get_transcript(session, transcript_id)
    if transcript:
        session.delete(transcript)
        session.commit()
        return True
    return False
