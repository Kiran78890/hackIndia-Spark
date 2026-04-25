import os
from google.cloud import translate_v2
from googletrans import Translator
from dotenv import load_dotenv
from core.constants import SUPPORTED_LANGUAGES

load_dotenv()

# Try to use Google Cloud Translator first
try:
    credentials_path = os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH', 'google-credentials.json')
    if os.path.exists(credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        google_translator = translate_v2.Client()
        USE_GOOGLE_CLOUD = True
        print("✅ Google Cloud Translator initialized")
    else:
        google_translator = None
        USE_GOOGLE_CLOUD = False
        print("⚠️ Google Cloud credentials not found, using fallback")
except Exception as e:
    google_translator = None
    USE_GOOGLE_CLOUD = False
    print(f"⚠️ Google Cloud Translator failed: {str(e)}, using fallback")

# Fallback translator
fallback_translator = Translator()

def detect_and_translate(text: str) -> tuple:
    """
    Detect language and translate to English if needed
    
    Args:
        text: Input text
        
    Returns:
        Tuple of (detected_language, translated_text)
    """
    try:
        # First, detect language
        detected_language = detect_language(text)
        
        print(f"🌐 Detected language: {detected_language}")
        
        # If already English, return as is
        if detected_language == 'en':
            return detected_language, text
        
        # Try Google Cloud Translator first
        if USE_GOOGLE_CLOUD and google_translator:
            try:
                result = google_translator.translate_text(
                    text,
                    source_language=detected_language,
                    target_language='en'
                )
                translated_text = result['translatedText']
                print(f"✅ Translated using Google Cloud Translator")
                return detected_language, translated_text
            except Exception as e:
                print(f"⚠️ Google Cloud failed: {str(e)}, trying fallback")
        
        # Fallback to googletrans
        translation = fallback_translator.translate(text, src_language=detected_language, dest_language='en')
        translated_text = translation['text']
        print(f"✅ Translated using googletrans")
        return detected_language, translated_text
        
    except Exception as e:
        print(f"❌ Translation error: {str(e)}")
        return 'unknown', text

def detect_language(text: str) -> str:
    """
    Detect language of text
    
    Args:
        text: Text to detect
        
    Returns:
        Language code (e.g., 'en', 'hi', 'es')
    """
    try:
        detection = fallback_translator.detect(text)
        lang = detection.get('lang') if isinstance(detection, dict) else detection.lang
        return lang if lang else 'en'
    except:
        return 'en'

def get_language_name(lang_code: str) -> str:
    """
    Convert language code to language name
    
    Args:
        lang_code: Language code (e.g., 'en', 'hi', 'es')
        
    Returns:
        Language name (e.g., 'English', 'Hindi', 'Spanish')
    """
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code.upper())