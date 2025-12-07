"""Transcription Service - handles audio transcription."""
from pathlib import Path
from typing import Literal

from app.adapters import ModelAdapter
from app.adapters.dummy_adapter import DummyAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.config import get_settings
from app.logger import logger

AdapterType = Literal["gemini", "dummy"]


def get_adapter(adapter_type: AdapterType = "dummy", api_key: str | None = None) -> ModelAdapter:
    """Get the appropriate model adapter.
    
    Args:
        adapter_type: Which adapter to use
        api_key: Optional API key override
        
    Returns:
        Model adapter instance
    """
    if adapter_type == "gemini":
        return GeminiAdapter(api_key=api_key)
    else:
        return DummyAdapter()


async def transcribe_audio(
    audio_path: Path | str,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> str:
    """Transcribe an audio file.
    
    Args:
        audio_path: Path to audio file
        adapter_type: Which adapter to use
        api_key: Optional API key for the adapter
        
    Returns:
        Raw transcription text
    """
    path = Path(audio_path) if isinstance(audio_path, str) else audio_path
    
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    
    logger.info(f"Transcribing {path} using {adapter_type} adapter")
    
    adapter = get_adapter(adapter_type, api_key)
    raw_text = await adapter.transcribe_audio(path)
    
    logger.info(f"Transcription complete: {len(raw_text)} chars")
    return raw_text


async def transcribe_audio_bytes(
    audio_bytes: bytes,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> str:
    """Transcribe audio bytes (writes to temp file)."""
    import tempfile
    import os
    
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = Path(tmp.name)
    
    try:
        return await transcribe_audio(tmp_path, adapter_type, api_key)
    finally:
        # Cleanup
        if tmp_path.exists():
            os.unlink(tmp_path)
