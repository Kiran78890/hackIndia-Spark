import os
import requests
from dotenv import load_dotenv

load_dotenv()

FACT_CHECK_API_KEY = os.getenv('FACT_CHECK_API_KEY')

def check_with_factcheck(text: str) -> dict:
    """
    Use Fact Check API to verify claims
    
    Args:
        text: Text/claim to fact-check
        
    Returns:
        Dictionary with fact-check results
    """
    try:
        if not FACT_CHECK_API_KEY:
            print("⚠️ Fact Check API key not found, using mock")
            return mock_factcheck(text)
        
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        
        params = {
            'query': text[:100],
            'key': FACT_CHECK_API_KEY,
            'languageCode': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            
            if claims:
                factcheck_results = []
                credibility_boost = 0
                
                for claim in claims[:3]:
                    claimReview = claim.get('claimReview', [{}])[0]
                    
                    result = {
                        'claim': claim.get('text', ''),
                        'rating': claimReview.get('textualRating', 'Unknown'),
                        'source': claimReview.get('publisher', {}).get('name', 'Unknown'),
                        'url': claimReview.get('url', ''),
                        'date': claim.get('claimDate', '')
                    }
                    factcheck_results.append(result)
                    
                    rating = result['rating'].lower()
                    if any(word in rating for word in ['true', 'correct', 'accurate']):
                        credibility_boost += 20
                    elif any(word in rating for word in ['false', 'incorrect', 'misleading']):
                        credibility_boost -= 20
                
                return {
                    "fact_checks": factcheck_results,
                    "credibility_boost": min(credibility_boost, 30),
                    "has_fact_checks": True
                }
            else:
                return {
                    "fact_checks": [],
                    "credibility_boost": 0,
                    "has_fact_checks": False
                }
        else:
            return {
                "fact_checks": [],
                "credibility_boost": 0,
                "has_fact_checks": False
            }
            
    except Exception as e:
        print(f"❌ Fact Check error: {str(e)}")
        return mock_factcheck(text)

def mock_factcheck(text: str) -> dict:
    """Mock fact-check (for testing without API key)"""
    return {
        "fact_checks": [],
        "credibility_boost": 0,
        "has_fact_checks": False
    }