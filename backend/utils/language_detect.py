from googletrans import Translator
from core.constants import SUPPORTED_LANGUAGES

translator = Translator()

def detect_language_code(text: str) -> str:
    """
    Detect language code from text
    
    Args:
        text: Text to detect
        
    Returns:
        Language code
    """
    try:
        detection = translator.detect(text)
        lang = detection.get('lang') if isinstance(detection, dict) else detection.lang
        return lang if lang else 'en'
    except:
        return 'en'

def get_language_full_name(lang_code: str) -> str:
    """Get full language name from code"""
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code.upper())