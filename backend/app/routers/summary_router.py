"""Summary Router - summary generation endpoints."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import summary_service

router = APIRouter(prefix="/summaries", tags=["summaries"])


class SummaryRequest(BaseModel):
    text: str
    adapter: str = "dummy"
    api_key: Optional[str] = None


class BulletsResponse(BaseModel):
    bullets: List[str]


class SummaryResponse(BaseModel):
    summary: str


@router.post("/bullets", response_model=BulletsResponse)
async def generate_bullets(data: SummaryRequest):
    """Generate bullet point summary from text."""
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    bullets = await summary_service.generate_bullets(
        data.text, data.adapter, data.api_key
    )
    
    return BulletsResponse(bullets=bullets)


@router.post("/long", response_model=SummaryResponse)
async def generate_long_summary(data: SummaryRequest):
    """Generate long-form summary from text."""
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    summary = await summary_service.generate_long_summary(
        data.text, data.adapter, data.api_key
    )
    
    return SummaryResponse(summary=summary)
