"""Idea Repository - CRUD operations for ideas."""
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.db import get_session
from app.models import Idea, IdeaStatus


def create_idea(session: Session, title: Optional[str] = None) -> Idea:
    """Create a new idea.
    
    Args:
        session: Database session
        title: Optional title
        
    Returns:
        Created idea
    """
    idea = Idea(title=title)
    session.add(idea)
    session.commit()
    session.refresh(idea)
    return idea


def get_idea(session: Session, idea_id: UUID) -> Optional[Idea]:
    """Get an idea by ID.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        
    Returns:
        Idea if found, None otherwise
    """
    return session.get(Idea, idea_id)


def get_all_ideas(session: Session) -> List[Idea]:
    """Get all ideas.
    
    Args:
        session: Database session
        
    Returns:
        List of all ideas
    """
    statement = select(Idea).order_by(Idea.created_at.desc())
    results = session.exec(statement)
    return list(results.all())


def update_idea_status(
    session: Session,
    idea_id: UUID,
    status: IdeaStatus
) -> Optional[Idea]:
    """Update an idea's status.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        status: New status
        
    Returns:
        Updated idea if found
    """
    idea = get_idea(session, idea_id)
    if idea:
        idea.status = status
        session.add(idea)
        session.commit()
        session.refresh(idea)
    return idea


def update_idea_audio_path(
    session: Session,
    idea_id: UUID,
    audio_path: str
) -> Optional[Idea]:
    """Update an idea's audio path.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        audio_path: Path to audio file
        
    Returns:
        Updated idea if found
    """
    idea = get_idea(session, idea_id)
    if idea:
        idea.audio_path = audio_path
        session.add(idea)
        session.commit()
        session.refresh(idea)
    return idea


def delete_idea(session: Session, idea_id: UUID) -> bool:
    """Delete an idea.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        
    Returns:
        True if deleted, False if not found
    """
    idea = get_idea(session, idea_id)
    if idea:
        session.delete(idea)
        session.commit()
        return True
    return False
