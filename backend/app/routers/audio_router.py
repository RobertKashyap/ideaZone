"""Audio Router - audio upload/download endpoints via DB."""
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from sqlmodel import Session

from app.db import get_session
from app.repos import idea_repo
from app.services import audio_service

router = APIRouter(prefix="/ideas", tags=["audio"])


@router.post("/{idea_id}/audio")
async def upload_audio(
    idea_id: UUID,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """Upload audio file for an idea (stored in DB)."""
    # Validate idea exists
    idea = idea_repo.get_idea(session, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    # Read file content
    audio_bytes = await file.read()
    
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    # Save audio to DB
    size = await audio_service.save_audio(session, idea_id, audio_bytes)
    
    return {
        "idea_id": str(idea_id),
        "size_bytes": size,
        "filename": file.filename,
        "message": "Audio saved to database"
    }


@router.get("/{idea_id}/audio/download")
async def download_audio(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Download/stream audio file from DB."""
    audio_bytes = audio_service.get_audio(session, idea_id)
    
    if not audio_bytes:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    return Response(
        content=audio_bytes,
        media_type="audio/webm"  # Assuming webm from frontend recorder
    )


@router.get("/{idea_id}/audio/status")
async def get_audio_status(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Check if audio exists for an idea."""
    has_audio = audio_service.audio_exists(session, idea_id)
    
    return {
        "idea_id": str(idea_id),
        "has_audio": has_audio
    }


@router.delete("/{idea_id}/audio")
async def delete_audio(
    idea_id: UUID,
    session: Session = Depends(get_session)
):
    """Delete audio file for an idea."""
    deleted = audio_service.delete_audio(session, idea_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    return {
        "idea_id": str(idea_id),
        "deleted": deleted
    }
