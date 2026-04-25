"""
LibreTranslate service - Fallback translation with public API
"""

import requests
from typing import Tuple
import json

# Public LibreTranslate instance
LIBRE_TRANSLATE_URL = "https://libretranslate.com"

# Alternative instances (if primary is down)
ALTERNATIVE_URLS = [
    "https://translate.argosopentech.com",
    "https://libretranslate.de",
]

def detect_language_libre(text: str) -> str:
    """
    Detect language using LibreTranslate
    
    Args:
        text: Text to detect language from
        
    Returns:
        Language code (e.g., 'en', 'hi', 'es')
    """
    try:
        response = requests.post(
            f"{LIBRE_TRANSLATE_URL}/detect",
            data={"q": text},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                lang_code = result[0].get("language", "en")
                confidence = result[0].get("confidence", 0)
                print(f"✅ LibreTranslate detected: {lang_code} (confidence: {confidence})")
                return lang_code
    except Exception as e:
        print(f"⚠️ LibreTranslate detection failed: {str(e)}")
    
    return "en"  # Default to English


def translate_text_libre(text: str, source_lang: str = "auto", target_lang: str = "en") -> Tuple[str, str]:
    """
    Translate text using LibreTranslate
    
    Args:
        text: Text to translate
        source_lang: Source language code (default: auto-detect)
        target_lang: Target language code (default: en)
        
    Returns:
        Tuple of (detected_language, translated_text)
    """
    
    if not text or len(text.strip()) == 0:
        return source_lang, text
    
    # If already in target language, return as is
    if source_lang == target_lang and source_lang != "auto":
        print(f"ℹ️  Text already in {target_lang}, skipping translation")
        return source_lang, text
    
    urls_to_try = [LIBRE_TRANSLATE_URL] + ALTERNATIVE_URLS
    
    for url in urls_to_try:
        try:
            print(f"📡 Trying LibreTranslate at: {url}")
            
            # Auto-detect if needed
            detected_lang = source_lang
            if source_lang == "auto":
                detected_lang = detect_language_libre(text)
            
            # Translate
            response = requests.post(
                f"{url}/translate",
                json={
                    "q": text,
                    "source": detected_lang,
                    "target": target_lang,
                    "format": "text"
                },
                timeout=10,
                headers={"User-Agent": "TruScan/1.0"}
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get("translatedText", text)
                print(f"✅ Translation successful from {detected_lang} to {target_lang}")
                return detected_lang, translated_text
            else:
                print(f"⚠️ Status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout from {url}, trying alternative...")
            continue
        except requests.exceptions.ConnectionError:
            print(f"🚫 Connection failed to {url}, trying alternative...")
            continue
        except Exception as e:
            print(f"❌ Error with {url}: {str(e)}")
            continue
    
    print(f"⚠️ All LibreTranslate instances failed, returning original text")
    return source_lang, text


def get_language_name(lang_code: str) -> str:
    """
    Convert language code to language name
    
    Args:
        lang_code: Language code (e.g., 'en', 'hi', 'es')
        
    Returns:
        Language name (e.g., 'English', 'Hindi', 'Spanish')
    """
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'bn': 'Bengali',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ml': 'Malayalam',
        'kn': 'Kannada',
        'gu': 'Gujarati',
        'mr': 'Marathi',
        'pa': 'Punjabi',
        'auto': 'Auto-detect',
        'unknown': 'Unknown'
    }
    
    return language_names.get(lang_code, lang_code.upper())