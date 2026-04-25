from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.scoring import calculate_score, get_verdict_details

router = APIRouter(prefix="/score", tags=["scoring"])

class ScoreCalculationRequest(BaseModel):
    """Request model for score calculation"""
    ai_confidence: int
    factcheck_boost: int = 0

@router.post("/calculate")
async def calculate_score_endpoint(request: ScoreCalculationRequest):
    """
    Calculate final score based on components
    
    Now only uses:
    - AI Confidence (70%)
    - Fact Check Boost (30%)
    """
    try:
        result = calculate_score(
            request.ai_confidence,
            factcheck_boost=request.factcheck_boost
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Score calculation failed: {str(e)}")

@router.get("/verdict/{score}")
async def get_verdict(score: int):
    """
    Get verdict details for a specific score
    
    - **score**: Score value (0-100)
    
    Returns verdict, emoji, and color
    """
    if score < 0 or score > 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    
    verdict = get_verdict_details(score)
    return verdict