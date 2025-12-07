"""Database models for Idea Tracker."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class IdeaStatus(str, Enum):
    """Idea lifecycle status."""
    DRAFT = "draft"
    TRANSCRIBED = "transcribed"
    APPROVED = "approved"
    RESEARCHING = "researching"
    COMPLETED = "completed"


class Idea(SQLModel, table=True):
    """Core idea entity."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: Optional[str] = None
    status: IdeaStatus = IdeaStatus.DRAFT
    audio_path: Optional[str] = None  # Deprecated, use audio_blob
    audio_blob: Optional[bytes] = Field(default=None, sa_column_kwargs={"type_": "LargeBinary"})
    audio_size: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Transcript(SQLModel, table=True):
    """Transcription of an idea's audio."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    idea_id: UUID = Field(foreign_key="idea.id")
    raw_text: str = ""
    cleaned_text: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    """Tag for categorizing ideas."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    confidence: float = 1.0


class Category(SQLModel, table=True):
    """Category for organizing ideas (e.g., B2B, B2C)."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None


class ResearchReport(SQLModel, table=True):
    """Research report generated for an idea."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    idea_id: UUID = Field(foreign_key="idea.id")
    report_json: str = "{}"  # JSON string for structured sections A-K
    summary: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
