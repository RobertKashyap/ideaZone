"""Idea Router - CRUD and lifecycle endpoints for ideas."""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.controllers import idea_pipeline
from app.db import get_session
from app.models import Idea, IdeaStatus
from app.repos import idea_repo

router = APIRouter(prefix="/ideas", tags=["ideas"])


# Request/Response models
class IdeaCreate(BaseModel):
    title: Optional[str] = None


class IdeaResponse(BaseModel):
    id: str
    title: Optional[str]
    status: str
    audio_path: Optional[str]
    created_at: str
    updated_at: str


class ProcessRequest(BaseModel):
    adapter: str = "dummy"
    api_key: Optional[str] = None


class ApprovalResponse(BaseModel):
    idea_id: str
    status: str
    message: str


def _idea_to_response(idea: Idea) -> IdeaResponse:
    """Convert Idea model to response."""
    return IdeaResponse(
        id=str(idea.id),
        title=idea.title,
        status=idea.status.value,
        audio_path=idea.audio_path,
        created_at=idea.created_at.isoformat(),
        updated_at=idea.updated_at.isoformat()
    )


@router.get("", response_model=List[IdeaResponse])
async def list_ideas(session: Session = Depends(get_session)):
    """List all ideas."""
    ideas = idea_repo.get_all_ideas(session)
    return [_idea_to_response(idea) for idea in ideas]


@router.post("", response_model=IdeaResponse)
async def create_idea(
    data: IdeaCreate = None,
    session: Session = Depends(get_session)
):
    """Create a new idea."""
    title = data.title if data else None
    idea = idea_repo.create_idea(session, title=title)
    return _idea_to_response(idea)


@router.get("/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Get an idea by ID."""
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return _idea_to_response(idea)


@router.delete("/{idea_id}")
async def delete_idea(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Delete an idea."""
    deleted = idea_repo.delete_idea(session, idea_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Idea not found")
    return {"deleted": True}


@router.post("/{idea_id}/process")
async def process_idea(
    idea_id: UUID,
    data: ProcessRequest = None,
    session: Session = Depends(get_session)
):
    """Full processing: transcribe, clean, summarize, tag."""
    adapter = data.adapter if data else "dummy"
    api_key = data.api_key if data else None
    
    try:
        result = await idea_pipeline.process_transcription(
            session, idea_id, adapter, api_key
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{idea_id}/approve", response_model=ApprovalResponse)
async def approve_idea(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Approve idea for research."""
    try:
        result = await idea_pipeline.approve_idea(session, idea_id)
        return ApprovalResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
