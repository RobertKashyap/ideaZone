"""Idea Pipeline Controller - orchestrates the full idea lifecycle."""
from typing import List, Literal, Optional, Tuple
from uuid import UUID

from sqlmodel import Session

from app.controllers import transcription_controller
from app.logger import logger
from app.models import IdeaStatus
from app.repos import idea_repo, transcript_repo
from app.services import summary_service, tagging_service

AdapterType = Literal["gemini", "dummy"]


async def process_transcription(
    session: Session,
    idea_id: UUID,
    adapter_type: AdapterType = "dummy",
    api_key: Optional[str] = None
) -> dict:
    """Process an idea: transcribe, clean, summarize, and tag.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        Dict with all processing results
    """
    logger.info(f"Processing idea {idea_id}")
    
    # Step 1: Transcribe and clean
    transcription_result = await transcription_controller.transcribe_and_clean(
        session, idea_id, adapter_type, api_key
    )
    
    cleaned_text = transcription_result["transcription_clean"]
    
    # Step 2: Generate summary bullets
    bullets = await summary_service.generate_bullets(
        cleaned_text, adapter_type, api_key
    )
    
    # Step 3: Generate long summary
    summary = await summary_service.generate_long_summary(
        cleaned_text, adapter_type, api_key
    )
    
    # Step 4: Suggest tags
    tags = await tagging_service.suggest_tags(
        cleaned_text, adapter_type, api_key
    )
    
    logger.info(f"Processing complete for idea {idea_id}")
    
    return {
        **transcription_result,
        "summary": summary,
        "bullets": bullets,
        "tags": [{"name": name, "confidence": conf} for name, conf in tags]
    }


async def approve_idea(
    session: Session,
    idea_id: UUID
) -> dict:
    """Approve an idea for research.
    
    Transitions status to APPROVED and enqueues research job.
    
    Args:
        session: Database session
        idea_id: Idea UUID
        
    Returns:
        Dict with approval status
    """
    logger.info(f"Approving idea {idea_id}")
    
    # Get idea
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise ValueError(f"Idea not found: {idea_id}")
    
    # Validate status transition
    if idea.status not in [IdeaStatus.TRANSCRIBED, IdeaStatus.DRAFT]:
        logger.warning(f"Idea {idea_id} status is {idea.status}, approving anyway")
    
    # Update status to approved
    idea_repo.update_idea_status(session, idea_id, IdeaStatus.APPROVED)
    
    # TODO: Enqueue research job (Phase 2)
    # For now, just mark as approved
    
    logger.info(f"Idea {idea_id} approved for research")
    
    return {
        "idea_id": str(idea_id),
        "status": IdeaStatus.APPROVED.value,
        "message": "Idea approved for research. Research job will be queued."
    }
