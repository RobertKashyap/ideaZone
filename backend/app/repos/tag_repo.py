"""Tag Repository - CRUD operations for tags."""
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import Tag


def create_tag(
    session: Session,
    name: str,
    confidence: float = 1.0
) -> Tag:
    """Create a new tag.
    
    Args:
        session: Database session
        name: Tag name
        confidence: Confidence score
        
    Returns:
        Created tag
    """
    tag = Tag(name=name, confidence=confidence)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def get_tag(session: Session, tag_id: UUID) -> Optional[Tag]:
    """Get a tag by ID.
    
    Args:
        session: Database session
        tag_id: Tag UUID
        
    Returns:
        Tag if found
    """
    return session.get(Tag, tag_id)


def get_tag_by_name(session: Session, name: str) -> Optional[Tag]:
    """Get a tag by name.
    
    Args:
        session: Database session
        name: Tag name
        
    Returns:
        Tag if found
    """
    statement = select(Tag).where(Tag.name == name)
    results = session.exec(statement)
    return results.first()


def get_or_create_tag(
    session: Session,
    name: str,
    confidence: float = 1.0
) -> Tag:
    """Get existing tag or create new one.
    
    Args:
        session: Database session
        name: Tag name
        confidence: Confidence score for new tags
        
    Returns:
        Tag (existing or new)
    """
    existing = get_tag_by_name(session, name)
    if existing:
        return existing
    return create_tag(session, name, confidence)


def get_all_tags(session: Session) -> List[Tag]:
    """Get all tags.
    
    Args:
        session: Database session
        
    Returns:
        List of all tags
    """
    statement = select(Tag).order_by(Tag.name)
    results = session.exec(statement)
    return list(results.all())


def delete_tag(session: Session, tag_id: UUID) -> bool:
    """Delete a tag.
    
    Args:
        session: Database session
        tag_id: Tag UUID
        
    Returns:
        True if deleted
    """
    tag = get_tag(session, tag_id)
    if tag:
        session.delete(tag)
        session.commit()
        return True
    return False
