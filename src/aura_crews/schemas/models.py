"""Pydantic models for crew I/O — structured outputs."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class CrewRequest(BaseModel):
    """Incoming request from Gateway."""
    task: str = Field(..., description="User message or task")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class CrewResponse(BaseModel):
    """Response back to Gateway."""
    success: bool = True
    response: str = ""
    crew: str = ""
    duration: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContentOutput(BaseModel):
    """Structured output for content crew."""
    hook: str = Field(description="Scroll-stopping first line")
    caption: str = Field(description="Main post body")
    cta: str = Field(description="Call-to-action")
    hashtags: List[str] = Field(default_factory=list, description="10-15 hashtags")
    visual_suggestion: str = Field(default="", description="Image/visual idea")
    platform: str = Field(default="Instagram", description="Best platform")


class ResearchOutput(BaseModel):
    """Structured output for research crew."""
    summary: str = Field(description="Executive summary")
    key_findings: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class ImagePromptOutput(BaseModel):
    """Structured output for image crew."""
    prompt: str = Field(description="Optimized image generation prompt")
    style: str = Field(default="")
    dimensions: str = Field(default="1024x1024")
    negative_prompt: str = Field(default="")


class FinanceOutput(BaseModel):
    """Structured output for finance crew."""
    analysis: str = Field(description="Financial analysis")
    figures: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    summary: str = Field(default="")
