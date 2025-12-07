"""Tag Router - tag suggestion endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.db import get_session
from app.repos import tag_repo
from app.services import tagging_service

router = APIRouter(prefix="/tags", tags=["tags"])


class SuggestRequest(BaseModel):
    text: str
    adapter: str = "dummy"
    api_key: Optional[str] = None


class TagSuggestion(BaseModel):
    name: str
    confidence: float


class SuggestResponse(BaseModel):
    tags: List[TagSuggestion]
    categories: List[str]


class TagResponse(BaseModel):
    id: str
    name: str
    confidence: float


@router.post("/suggest", response_model=SuggestResponse)
async def suggest_tags(data: SuggestRequest):
    """Suggest tags for the given text."""
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    tags = await tagging_service.suggest_tags(
        data.text, data.adapter, data.api_key
    )
    
    # Get predefined categories
    all_categories = tagging_service.get_predefined_categories()
    
    return SuggestResponse(
        tags=[TagSuggestion(name=name, confidence=conf) for name, conf in tags],
        categories=all_categories
    )


@router.get("", response_model=List[TagResponse])
async def list_tags(session: Session = Depends(get_session)):
    """List all saved tags."""
    tags = tag_repo.get_all_tags(session)
    return [
        TagResponse(id=str(tag.id), name=tag.name, confidence=tag.confidence)
        for tag in tags
    ]


@router.get("/categories")
async def list_categories():
    """List predefined categories."""
    return {"categories": tagging_service.get_predefined_categories()}
