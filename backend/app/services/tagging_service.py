"""Tagging Service - suggests tags and categories for ideas."""
from typing import List, Literal, Tuple

from app.adapters.dummy_adapter import DummyAdapter
from app.adapters.gemini_adapter import GeminiAdapter
from app.logger import logger

AdapterType = Literal["gemini", "dummy"]

# Pre-defined categories
PREDEFINED_CATEGORIES = [
    "B2B",
    "B2C",
    "SaaS",
    "Marketplace",
    "Mobile App",
    "E-commerce",
    "AI/ML",
    "Health & Wellness",
    "Finance",
    "Education",
    "Productivity",
    "Social",
    "Entertainment",
    "Hardware",
    "Developer Tools",
]


def get_adapter(adapter_type: AdapterType = "dummy", api_key: str | None = None):
    """Get the appropriate model adapter."""
    if adapter_type == "gemini":
        return GeminiAdapter(api_key=api_key)
    return DummyAdapter()


async def suggest_tags(
    text: str,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> List[Tuple[str, float]]:
    """Suggest tags for the given text.
    
    Args:
        text: Input text to analyze
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        List of (tag, confidence) tuples, sorted by confidence
    """
    logger.info(f"Suggesting tags using {adapter_type} adapter")
    
    adapter = get_adapter(adapter_type, api_key)
    tags = await adapter.suggest_tags(text)
    
    # Sort by confidence
    tags_sorted = sorted(tags, key=lambda x: x[1], reverse=True)
    
    logger.info(f"Suggested {len(tags_sorted)} tags")
    return tags_sorted


async def suggest_categories(
    text: str,
    adapter_type: AdapterType = "dummy",
    api_key: str | None = None
) -> List[Tuple[str, float]]:
    """Suggest categories from predefined list.
    
    Args:
        text: Input text to analyze
        adapter_type: Which adapter to use
        api_key: Optional API key
        
    Returns:
        List of (category, confidence) tuples from predefined categories
    """
    # Get all tags
    all_tags = await suggest_tags(text, adapter_type, api_key)
    
    # Filter to only predefined categories
    categories = [
        (tag, conf) for tag, conf in all_tags
        if tag in PREDEFINED_CATEGORIES
    ]
    
    return categories


def get_predefined_categories() -> List[str]:
    """Get list of predefined categories."""
    return PREDEFINED_CATEGORIES.copy()
