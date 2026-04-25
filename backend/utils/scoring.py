from core.constants import VERDICT_RANGES, VERDICTS, COLORS

def calculate_score(
    ai_confidence: int,
    sources_found: int = 0,
    credibility_score: int = 0,
    factcheck_boost: int = 0
) -> dict:
    """
    Calculate final fake/real score
    
    Args:
        ai_confidence: AI reasoning confidence (0-100)
        sources_found: DEPRECATED (kept for compatibility)
        credibility_score: DEPRECATED (kept for compatibility)
        factcheck_boost: Boost from fact-check API
        
    Returns:
        Dictionary with final score and verdict
    """
    
    # Updated weight distribution (no source verification)
    ai_weight = 0.70        # 70% - AI reasoning (was 40%)
    factcheck_weight = 0.30 # 30% - Fact checking (was 25%)
    
    # Normalize scores
    ai_score = ai_confidence
    
    # Fact-check score
    factcheck_score = 50 + factcheck_boost
    factcheck_score = min(100, max(0, factcheck_score))
    
    # Calculate weighted final score
    final_score = int(
        (ai_score * ai_weight) + 
        (factcheck_score * factcheck_weight)
    )
    final_score = min(100, max(0, final_score))
    
    # Determine verdict
    if final_score < 40:
        verdict_key = 'fake'
    elif final_score < 70:
        verdict_key = 'suspicious'
    else:
        verdict_key = 'real'
    
    return {
        "final_score": final_score,
        "verdict": VERDICTS[verdict_key],
        "color": COLORS[verdict_key],
        "breakdown": {
            "ai_score": ai_score,
            "factcheck_score": factcheck_score,
            "sources_found": 0  # Always 0 now
        }
    }

def get_verdict_details(score: int) -> dict:
    """Get verdict details for a score"""
    if score < 40:
        return {"verdict": "FAKE", "emoji": "🚨", "color": "red"}
    elif score < 70:
        return {"verdict": "SUSPICIOUS", "emoji": "⚠️", "color": "yellow"}
    else:
        return {"verdict": "REAL", "emoji": "✅", "color": "green"}