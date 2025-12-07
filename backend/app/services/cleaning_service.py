"""Cleaning Service - removes filler words and normalizes text."""
import re
from typing import List

# Common filler words and phrases to remove
FILLER_WORDS = [
    r"\bum+\b",
    r"\buh+\b",
    r"\bah+\b",
    r"\beh+\b",
    r"\blike\b(?=\s+like\b)",  # repeated "like like"
    r"\byou know\b",
    r"\bi mean\b",
    r"\bbasically\b",
    r"\bactually\b",
    r"\bliterally\b",
    r"\bso+\b(?=\s+so\b)",  # repeated "so so"
    r"\bwell\b(?=\s+well\b)",  # repeated "well well"
]


def remove_fillers(text: str) -> str:
    """Remove filler words from transcript.
    
    Args:
        text: Raw transcript text
        
    Returns:
        Text with filler words removed
    """
    cleaned = text
    
    for pattern in FILLER_WORDS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    # Remove excessive punctuation
    cleaned = re.sub(r"[,]{2,}", ",", cleaned)
    cleaned = re.sub(r"[.]{2,}", ".", cleaned)
    
    # Normalize whitespace
    cleaned = normalize_whitespace(cleaned)
    
    return cleaned


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.
    
    - Collapses multiple spaces into single space
    - Removes leading/trailing whitespace
    - Normalizes newlines
    """
    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Clean up space around punctuation
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"([.,!?;:])\s*([A-Z])", r"\1 \2", text)
    
    return text.strip()


def clean_transcript(text: str) -> str:
    """Full transcript cleaning pipeline.
    
    Applies all cleaning operations.
    """
    cleaned = remove_fillers(text)
    cleaned = normalize_whitespace(cleaned)
    return cleaned
