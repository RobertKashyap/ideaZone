"""Dummy Adapter - mock implementation for testing without API keys."""
import random
from pathlib import Path
from typing import List, Tuple

from app.adapters import ModelAdapter

# Sample transcripts for testing
MOCK_TRANSCRIPTS = [
    """So I've been thinking about this idea for a while now. Um, basically, 
    it's like an app that helps people track their daily habits. You know, 
    like a habit tracker but with AI-powered insights. The AI would analyze 
    your patterns and suggest optimal times for different activities. 
    I think it could be really useful for productivity.""",
    
    """Okay so here's my idea. It's a platform for connecting freelancers 
    with local businesses. Uh, like, think of it as Uber but for skilled 
    trades. Plumbers, electricians, that kind of thing. The differentiator 
    is real-time availability and instant booking with verified professionals.""",
    
    """I want to build a sustainable fashion marketplace. The idea is to 
    create a platform where people can buy and sell pre-owned designer items, 
    but with authentication and quality verification. We'd use AI to verify 
    authenticity and provide fair pricing based on condition and market data.""",
]

MOCK_TAGS = [
    ("B2C", 0.9),
    ("Mobile App", 0.85),
    ("AI/ML", 0.8),
    ("SaaS", 0.75),
    ("Marketplace", 0.7),
    ("Health & Wellness", 0.65),
    ("Productivity", 0.6),
    ("E-commerce", 0.55),
]


class DummyAdapter(ModelAdapter):
    """Mock adapter for testing without API keys."""
    
    async def transcribe_audio(self, audio_path: Path) -> str:
        """Return a random mock transcript."""
        return random.choice(MOCK_TRANSCRIPTS)
    
    async def summarize_text(self, text: str) -> str:
        """Generate a simple summary."""
        sentences = text.replace("\n", " ").split(".")
        # Take first 2 sentences as summary
        summary = ". ".join(sentences[:2]).strip()
        if summary and not summary.endswith("."):
            summary += "."
        return summary
    
    async def generate_bullets(self, text: str) -> List[str]:
        """Generate mock bullet points."""
        return [
            "Core concept: AI-powered solution for everyday problems",
            "Target market: Consumers seeking efficiency",
            "Key differentiator: Smart automation and insights",
            "Revenue model: Subscription-based SaaS",
            "MVP scope: Mobile-first with basic features",
        ]
    
    async def suggest_tags(self, text: str) -> List[Tuple[str, float]]:
        """Return random subset of mock tags."""
        num_tags = random.randint(3, 6)
        return random.sample(MOCK_TAGS, min(num_tags, len(MOCK_TAGS)))
