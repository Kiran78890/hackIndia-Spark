import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

def check_with_huggingface(text: str) -> dict:
    """
    Use Hugging Face models for text classification
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with classification results
    """
    try:
        if not HUGGINGFACE_API_KEY:
            print("⚠️ Hugging Face API key not found")
            return mock_huggingface_check(text)
        
        # Using zero-shot classification model
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": ["fake news", "real news", "misinformation", "factual"]
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Hugging Face Classification Complete")
            return {
                "classification": result,
                "source": "Hugging Face"
            }
        else:
            return mock_huggingface_check(text)
            
    except Exception as e:
        print(f"❌ Hugging Face error: {str(e)}")
        return mock_huggingface_check(text)

def mock_huggingface_check(text: str) -> dict:
    """Mock HF check"""
    return {
        "classification": {"labels": ["real news", "fake news"], "scores": [0.7, 0.3]},
        "source": "Mock Hugging Face"
    }