"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint.
    
    Returns:
        dict: Status message indicating the API is running.
    """
    return {"status": "ok"}
