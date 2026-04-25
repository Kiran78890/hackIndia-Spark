from fastapi import APIRouter, File, UploadFile, HTTPException
from services.speechtotext import transcribe_audio
from services.verification import verify_complete

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/transcribe")
async def transcribe_only(audio: UploadFile = File(...)):
    """
    Just transcribe audio to text (no verification)
    
    - **audio**: Audio file (MP3, WAV, M4A, etc.)
    
    Returns transcribed text
    """
    try:
        result = transcribe_audio(audio.file)
        
        if result.get('error'):
            raise HTTPException(status_code=400, detail=result['text'])
        
        return {"text": result['text']}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.post("/verify")
async def verify_voice(audio: UploadFile = File(...)):
    """
    Transcribe audio and verify it for fake news
    
    1. Transcribe audio to text
    2. Run verification on text
    
    - **audio**: Audio file (MP3, WAV, M4A, etc.)
    """
    try:
        # Transcribe audio
        result = transcribe_audio(audio.file)
        
        if result.get('error'):
            raise HTTPException(status_code=400, detail=result['text'])
        
        transcribed_text = result['text']
        
        # Verify the transcribed text
        verification_result = await verify_complete(transcribed_text, use_mock=False)
        
        return {
            "transcribed_text": transcribed_text,
            "verification": verification_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice verification failed: {str(e)}")