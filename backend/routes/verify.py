from fastapi import APIRouter, HTTPException
from models.requestmodels import VerifyTextRequest
from models.responsemodels import (
    VerifyTextResponse, SourceModel, FactCheckModel, ScoreBreakdownModel
)
from services.verification import verify_complete

router = APIRouter(prefix="/api/verify", tags=["verification"])

@router.post("/text", response_model=VerifyTextResponse)
async def verify_text(request: VerifyTextRequest):
    """
    Verify text for fake news
    
    - **text**: The news claim to verify (max 2000 chars)
    - **use_mock**: Use mock data if True (for testing without API keys)
    """
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 2000:
        raise HTTPException(status_code=400, detail="Text too long (max 2000 characters)")
    
    try:
        result = await verify_complete(request.text)
        
        # Convert to response models
        fact_checks = [FactCheckModel(**fc) for fc in result.get('fact_checks', [])]
        news_sources = [SourceModel(**src) for src in result.get('news_sources', [])]
        
        return VerifyTextResponse(
            original_text=result['original_text'],
            translated_text=result['translated_text'],
            detected_language=result['detected_language'],
            ai_reasoning=result['ai_reasoning'],
            ai_source=result['ai_source'],
            fact_checks=fact_checks,
            news_sources=news_sources,
            final_score=result['final_score'],
            verdict=result['verdict'],
            color=result['color'],
            breakdown=ScoreBreakdownModel(**result['breakdown'])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")