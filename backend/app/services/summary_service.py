"""Summary Service - generates summaries and bullet points."""
from typing import List, Literal

from app.adapters.dummy_adapter import DummyAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.logger import logger

AdapterType = Literal["gemini", "dummy"]


def get_adapter(adapter_type: AdapterType = "dummy", api_key: str | None = None):
    """Get the appropriate model adapter."""
    if adapter_type == "gemini":
        return GeminiAdapter(api_key=api_key)
    return DummyAdapter()


async def generate_bullets(
    text: str,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> List[str]:
    """Generate bullet point summary from text.
    
    Args:
        text: Input text to summarize
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        List of 3-8 bullet points
    """
    logger.info(f"Generating bullets using {adapter_type} adapter")
    
    adapter = get_adapter(adapter_type, api_key)
    bullets = await adapter.generate_bullets(text)
    
    logger.info(f"Generated {len(bullets)} bullet points")
    return bullets


async def generate_long_summary(
    text: str,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> str:
    """Generate a longer summary paragraph.
    
    Args:
        text: Input text to summarize
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        Summary text (2-3 sentences)
    """
    logger.info(f"Generating summary using {adapter_type} adapter")
    
    adapter = get_adapter(adapter_type, api_key)
    summary = await adapter.summarize_text(text)
    
    logger.info(f"Generated summary: {len(summary)} chars")
    return summary
