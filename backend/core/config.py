import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the application"""
    
    # API Keys (Google Cloud removed)
    GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
    FACT_CHECK_API_KEY = os.getenv('FACT_CHECK_API_KEY')
    # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    # LibreTranslate Configuration (NEW)
    LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL', 'https://libretranslate.com')
    
    # App Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Limits
    MAX_TEXT_LENGTH = 2000
    MAX_AUDIO_SIZE_MB = 25
    
    # API Endpoints (Google Cloud removed)
    FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models"

settings = Settings()