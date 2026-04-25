import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the application"""
    
    # API Keys
    GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
    GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    GOOGLE_CLOUD_CREDENTIALS_PATH = os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH', 'google-credentials.json')
    FACT_CHECK_API_KEY = os.getenv('FACT_CHECK_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    # App Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Limits
    MAX_TEXT_LENGTH = 2000
    MAX_AUDIO_SIZE_MB = 25
    
    # API Endpoints
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models"

settings = Settings()