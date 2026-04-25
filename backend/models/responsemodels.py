from pydantic import BaseModel
from typing import List, Optional

class SourceModel(BaseModel):
    """News source model"""
    source: str
    title: str
    url: str
    publishedAt: str

class FactCheckModel(BaseModel):
    """Fact check result model"""
    claim: str
    rating: str
    source: str
    url: str
    date: str

class ScoreBreakdownModel(BaseModel):
    """Score breakdown model"""
    ai_score: int
    factcheck_score: int
    sources_found: int  # Will always be 0

class VerifyTextResponse(BaseModel):
    """Response model for text verification"""
    original_text: str
    translated_text: str
    detected_language: str
    ai_reasoning: str
    ai_source: str
    fact_checks: List[FactCheckModel]
    news_sources: List[SourceModel]  # Will always be empty
    final_score: int
    verdict: str
    color: str
    breakdown: ScoreBreakdownModel

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None