"""Router aggregator."""
from fastapi import APIRouter

from app.routers.audio_router import router as audio_router
from app.routers.health import router as health_router
from app.routers.idea_router import router as idea_router
from app.routers.summary_router import router as summary_router
from app.routers.tag_router import router as tag_router
from app.routers.transcription_router import router as transcription_router

# Main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health_router, tags=["health"])
api_router.include_router(idea_router)
api_router.include_router(audio_router)
api_router.include_router(transcription_router)
api_router.include_router(summary_router)
api_router.include_router(tag_router)

