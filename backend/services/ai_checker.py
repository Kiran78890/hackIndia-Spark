import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def check_with_gemini(text: str) -> dict:
    """
    Use Google Gemini to analyze if text is fake or real
    
    Args:
        text: Translated text to check
        
    Returns:
        Dictionary with reasoning and confidence score
    """
    try:
        if not GEMINI_API_KEY:
            print("⚠️ Gemini API key not found, using mock")
            return mock_gemini_check(text)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""You are a fact-checking expert. Analyze the following claim and determine if it's likely to be fake news or real news.

CLAIM: "{text}"

Provide your analysis in this EXACT format:
REALISTIC: [Yes/No/Maybe]
MISINFORMATION_PATTERN: [Yes/No/Unclear]
RED_FLAGS: [List 3 red flags or "None"]
CONFIDENCE: [0-100]
EXPLANATION: [1-2 sentence summary]

Be concise and clear."""

        response = model.generate_content(prompt)
        reasoning = response.text
        
        # Extract confidence score
        confidence = extract_gemini_confidence(reasoning)
        
        print(f"✅ Gemini Analysis Complete (Confidence: {confidence})")
        
        return {
            "reasoning": reasoning,
            "ai_confidence": confidence,
            "source": "Google Gemini"
        }
        
    except Exception as e:
        print(f"❌ Gemini error: {str(e)}")
        return mock_gemini_check(text)

def extract_gemini_confidence(text: str) -> int:
    """
    Extract confidence score from Gemini response
    
    Args:
        text: Gemini response text
        
    Returns:
        Confidence score (0-100)
    """
    try:
        match = re.search(r'CONFIDENCE:\s*(\d+)', text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return min(100, max(0, score))
    except:
        pass
    
    return 50