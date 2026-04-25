"""
Main verification orchestration service
Combines all services for complete verification
"""

from services.translation import detect_and_translate, get_language_name
from services.ai_checker import check_with_gemini
from services.hf import check_with_huggingface
from services.factcheck import check_with_factcheck
from utils.scoring import calculate_score

async def verify_complete(text: str, use_mock: bool = False) -> dict:
    """
    Complete verification pipeline
    
    Args:
        text: Input text to verify
        use_mock: Use mock data if True
        
    Returns:
        Complete verification result
    """
    
    print(f"\n{'='*60}")
    print(f"🔍 VERIFICATION STARTED")
    print(f"{'='*60}")
    
    try:
        # Step 1: Language Detection & Translation
        print(f"\n📝 STEP 1: Language Detection & Translation")
        detected_language, translated_text = detect_and_translate(text)
        language_name = get_language_name(detected_language)
        print(f"   ✅ Language: {language_name}")
        
        # Step 2: AI Analysis (Gemini)
        print(f"\n🤖 STEP 2: AI Analysis (Google Gemini)")
        if use_mock:
            from services.ai_checker import mock_gemini_check
            ai_result = mock_gemini_check(translated_text)
            print(f"   📌 MOCK MODE")
        else:
            ai_result = check_with_gemini(translated_text)
        
        ai_confidence = ai_result.get('ai_confidence', 50)
        
        # Step 3: Fact Checking
        print(f"\n📋 STEP 3: Fact Check Verification")
        if use_mock:
            from services.factcheck import mock_factcheck
            factcheck_result = mock_factcheck(translated_text)
        else:
            factcheck_result = check_with_factcheck(translated_text)
        
        factcheck_boost = factcheck_result.get('credibility_boost', 0)
        
        # Step 4: Calculate Score (without source verification)
        print(f"\n📊 STEP 4: Calculating Final Score")
        score_result = calculate_score(
            ai_confidence,
            sources_found=0,  # Set to 0 since we're not checking sources
            credibility_score=0,
            factcheck_boost=factcheck_boost
        )
        
        print(f"   ✅ FINAL SCORE: {score_result['final_score']}/100")
        print(f"   ✅ VERDICT: {score_result['verdict']}")
        print(f"{'='*60}\n")
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "detected_language": language_name,
            "ai_reasoning": ai_result.get('reasoning', ''),
            "ai_source": ai_result.get('source', 'Unknown'),
            "fact_checks": factcheck_result.get('fact_checks', []),
            "news_sources": [],  # Empty array since we're not checking sources
            "final_score": score_result['final_score'],
            "verdict": score_result['verdict'],
            "color": score_result['color'],
            "breakdown": score_result['breakdown']
        }
        
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        raise