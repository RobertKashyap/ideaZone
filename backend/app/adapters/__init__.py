"""Model Adapter Interface - defines contract for AI model adapters."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple


class ModelAdapter(ABC):
    """Abstract base class for AI model adapters."""
    
    @abstractmethod
    async def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Raw transcription text
        """
        pass
    
    @abstractmethod
    async def summarize_text(self, text: str) -> str:
        """Generate a summary of text.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Summary text
        """
        pass
    
    @abstractmethod
    async def generate_bullets(self, text: str) -> List[str]:
        """Generate bullet point summary.
        
        Args:
            text: Input text
            
        Returns:
            List of bullet points
        """
        pass
    
    @abstractmethod
    async def suggest_tags(self, text: str) -> List[Tuple[str, float]]:
        """Suggest tags for text.
        
        Args:
            text: Input text
            
        Returns:
            List of (tag, confidence) tuples
        """
        pass
