"""
Translation API endpoints using LibreTranslate
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.libretranslate_service import (
    translate_text_libre,
    detect_language_libre,
    get_language_name
)

router = APIRouter(prefix="/api/translate", tags=["translation"])

class TranslateRequest(BaseModel):
    """Request model for translation"""
    text: str
    source_language: str = "auto"
    target_language: str = "en"

class DetectRequest(BaseModel):
    """Request model for language detection"""
    text: str

@router.post("/detect")
async def detect_language(request: DetectRequest):
    """
    Detect language of given text using LibreTranslate
    
    - **text**: Text to detect language from
    
    Returns detected language code and name
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        detected_lang = detect_language_libre(request.text)
        language_name = get_language_name(detected_lang)
        
        return {
            "language_code": detected_lang,
            "language_name": language_name,
            "text_preview": request.text[:50] + "..." if len(request.text) > 50 else request.text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


@router.post("/text")
async def translate(request: TranslateRequest):
    """
    Translate text from source language to target language using LibreTranslate
    
    - **text**: Text to translate
    - **source_language**: Source language code (default: auto-detect)
    - **target_language**: Target language code (default: en)
    
    Returns translated text and detected language
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) > 5000:
            raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
        
        detected_lang, translated_text = translate_text_libre(
            request.text,
            source_lang=request.source_language,
            target_lang=request.target_language
        )
        
        language_name = get_language_name(detected_lang)
        target_lang_name = get_language_name(request.target_language)
        
        return {
            "original_text": request.text,
            "translated_text": translated_text,
            "source_language": {
                "code": detected_lang,
                "name": language_name
            },
            "target_language": {
                "code": request.target_language,
                "name": target_lang_name
            },
            "is_translated": detected_lang != request.target_language
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")