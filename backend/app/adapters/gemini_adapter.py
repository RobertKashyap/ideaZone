"""Gemini Adapter - LangChain integration with Google Gemini."""
import base64
from pathlib import Path
from typing import List, Tuple

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.adapters import ModelAdapter
from app.config import get_settings
from app.logger import logger


class GeminiAdapter(ModelAdapter):
    """Adapter for Google Gemini using LangChain."""
    
    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-flash"):
        """Initialize with API key and model.
        
        Args:
            api_key: Gemini API key (uses config/.env if not provided)
            model: Model name to use
        """
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = model
        
        if not self.api_key:
            logger.warning("No Gemini API key configured. Set GEMINI_API_KEY in .env")
        
        # Initialize LangChain ChatGoogleGenerativeAI
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            temperature=0.7,
            max_output_tokens=2048,
        ) if self.api_key else None
    
    async def _invoke(self, prompt: str, audio_path: Path | None = None) -> str:
        """Invoke LangChain model with text and optional audio.
        
        Args:
            prompt: Text prompt
            audio_path: Optional audio file to include
            
        Returns:
            Generated text response
        """
        if not self.llm:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY in .env")
        
        # Build message content
        content = []
        
        # Add audio if provided (as base64 for multimodal)
        if audio_path and audio_path.exists():
            with open(audio_path, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode("utf-8")
            
            content.append({
                "type": "media",
                "mime_type": "audio/mpeg",
                "data": audio_data,
            })
        
        # Add text prompt
        content.append({"type": "text", "text": prompt})
        
        # Create message and invoke
        message = HumanMessage(content=content)
        
        logger.debug(f"Invoking LangChain Gemini with prompt: {prompt[:100]}...")
        
        # Use ainvoke for async
        response = await self.llm.ainvoke([message])
        
        return response.content if response.content else ""
    
    async def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio using Gemini via LangChain."""
        prompt = """Transcribe this audio recording accurately. 
        Include all spoken words exactly as said.
        Do not add any commentary or formatting, just the raw transcription."""
        
        logger.info(f"Transcribing audio: {audio_path}")
        return await self._invoke(prompt, audio_path)
    
    async def summarize_text(self, text: str) -> str:
        """Generate summary using Gemini via LangChain."""
        prompt = f"""Summarize the following text in 2-3 sentences:

{text}

Summary:"""
        
        return await self._invoke(prompt)
    
    async def generate_bullets(self, text: str) -> List[str]:
        """Generate bullet points using Gemini via LangChain."""
        prompt = f"""Extract 3-8 key points from the following text as bullet points.
Each bullet should be concise (one sentence max).
Return ONLY the bullet points, one per line, starting with "- ".

Text:
{text}

Bullet points:"""
        
        response = await self._invoke(prompt)
        
        # Parse bullet points
        bullets = []
        for line in response.strip().split("\n"):
            line = line.strip()
            if line.startswith("- "):
                bullets.append(line[2:])
            elif line.startswith("• "):
                bullets.append(line[2:])
            elif line and not line.startswith("#"):
                bullets.append(line)
        
        return bullets[:8]  # Limit to 8
    
    async def suggest_tags(self, text: str) -> List[Tuple[str, float]]:
        """Suggest tags using Gemini via LangChain."""
        prompt = f"""Analyze this text and suggest relevant tags/categories.
For each tag, provide a confidence score from 0.0 to 1.0.
Use these categories if applicable: B2B, B2C, SaaS, Mobile App, E-commerce, 
Marketplace, AI/ML, Health, Finance, Education, Productivity, Social.

Format: TAG_NAME: CONFIDENCE
One per line, max 6 tags.

Text:
{text}

Tags:"""
        
        response = await self._invoke(prompt)
        
        # Parse tags
        tags = []
        for line in response.strip().split("\n"):
            if ":" in line:
                parts = line.split(":")
                tag = parts[0].strip().strip("-•")
                try:
                    confidence = float(parts[1].strip())
                    tags.append((tag, min(1.0, max(0.0, confidence))))
                except (ValueError, IndexError):
                    tags.append((tag, 0.7))
        
        return tags[:6]
