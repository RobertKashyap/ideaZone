"""Audio Service - handles audio file storage and retrieval via DB."""
from uuid import UUID

from sqlmodel import Session

from app.logger import logger
from app.models import Idea
from app.repos import idea_repo


async def save_audio(session: Session, idea_id: UUID, audio_bytes: bytes) -> int:
    """Save audio bytes to database.
    
    Args:
        session: DB session
        idea_id: The idea UUID
        audio_bytes: Raw audio data
        
    Returns:
        Size of saved audio in bytes
    """
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise ValueError(f"Idea not found: {idea_id}")
    
    idea.audio_blob = audio_bytes
    idea.audio_size = len(audio_bytes)
    # Clear old path if exists
    idea.audio_path = None
    
    session.add(idea)
    session.commit()
    session.refresh(idea)
    
    logger.info(f"Saved audio for idea {idea_id}: {len(audio_bytes)} bytes")
    return len(audio_bytes)


def get_audio(session: Session, idea_id: UUID) -> bytes | None:
    """Get audio bytes from database.
    
    Args:
        session: DB session
        idea_id: Idea UUID
        
    Returns:
        Audio bytes if found, None otherwise
    """
    idea = idea_repo.get_idea(session, idea_id)
    if not idea or not idea.audio_blob:
        return None
    
    return idea.audio_blob


def audio_exists(session: Session, idea_id: UUID) -> bool:
    """Check if audio exists for an idea."""
    idea = idea_repo.get_idea(session, idea_id)
    return bool(idea and idea.audio_blob)


def delete_audio(session: Session, idea_id: UUID) -> bool:
    """Delete audio from database.
    
    Returns:
        True if deleted
    """
    idea = idea_repo.get_idea(session, idea_id)
    if not idea or not idea.audio_blob:
        return False
    
    idea.audio_blob = None
    idea.audio_size = None
    idea.audio_path = None
    
    session.add(idea)
    session.commit()
    
    logger.info(f"Deleted audio for idea {idea_id}")
    return True
