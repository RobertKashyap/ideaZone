"""Router aggregator."""
from fastapi import APIRouter

from app.routers.health import router as health_router

# Main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health_router, tags=["health"])
