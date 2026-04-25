"""
Translation service - Uses LibreTranslate as primary, googletrans as fallback
Completely removed Google Cloud dependencies
"""

from services.libretranslate_service import (
    translate_text_libre, 
    detect_language_libre,
    get_language_name as get_lang_name_libre
)
from googletrans import Translator
from dotenv import load_dotenv
from core.constants import SUPPORTED_LANGUAGES

load_dotenv()

# Fallback translator (googletrans)
fallback_translator = Translator()

def detect_and_translate(text: str) -> tuple:
    """
    Detect language and translate to English if needed
    
    Priority order:
    1. LibreTranslate (free, reliable) ✅ PRIMARY
    2. googletrans (fallback - always works)
    
    Args:
        text: Input text
        
    Returns:
        Tuple of (detected_language, translated_text)
    """
    try:
        print(f"\n{'='*60}")
        print(f"📝 TRANSLATION PIPELINE STARTED")
        print(f"{'='*60}")
        
        # Step 1: Detect language using LibreTranslate
        print(f"\n🔍 Step 1: Language Detection")
        detected_language = detect_language_libre(text)
        print(f"   ✅ Detected: {detected_language}")
        
        # If already English, return as is
        if detected_language == 'en':
            print(f"   ℹ️  Text already in English, skipping translation")
            print(f"{'='*60}\n")
            return detected_language, text
        
        # Step 2: Try LibreTranslate first (primary translator)
        print(f"\n🌍 Step 2: Translation with LibreTranslate (Primary)")
        try:
            _, translated_text = translate_text_libre(
                text,
                source_lang=detected_language,
                target_lang='en'
            )
            print(f"   ✅ Translation successful")
            print(f"{'='*60}\n")
            return detected_language, translated_text
        except Exception as e:
            print(f"   ⚠️ LibreTranslate failed: {str(e)}")
        
        # Step 3: Fallback to googletrans
        print(f"\n📚 Step 3: Fallback Translation with googletrans")
        try:
            translation = fallback_translator.translate(
                text, 
                src_language=detected_language, 
                dest_language='en'
            )
            translated_text = translation['text']
            print(f"   ✅ Fallback translation successful")
            print(f"{'='*60}\n")
            return detected_language, translated_text
        except Exception as e:
            print(f"   ❌ Fallback failed: {str(e)}")
        
        print(f"   ⚠️ All translation services failed, returning original text")
        print(f"{'='*60}\n")
        return detected_language, text
        
    except Exception as e:
        print(f"❌ Translation error: {str(e)}")
        print(f"{'='*60}\n")
        return 'unknown', text


def detect_language(text: str) -> str:
    """
    Detect language of text
    Priority: LibreTranslate > googletrans
    
    Args:
        text: Text to detect
        
    Returns:
        Language code (e.g., 'en', 'hi', 'es')
    """
    try:
        # Try LibreTranslate first (preferred)
        lang = detect_language_libre(text)
        if lang and lang != 'unknown':
            return lang
    except:
        print("⚠️ LibreTranslate detection failed, using fallback")
    
    try:
        # Fallback to googletrans
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