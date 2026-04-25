import whisper
import os
from pathlib import Path

# Load the model (first time downloads ~140MB)
# Options: tiny, base, small, medium, large
# tiny = fastest, large = most accurate
try:
    model = whisper.load_model("base")  # ~140MB, good balance
    WHISPER_AVAILABLE = True
    print("✅ Whisper model loaded successfully")
except Exception as e:
    print(f"⚠️ Whisper loading failed: {str(e)}")
    model = None
    WHISPER_AVAILABLE = False

def transcribe_audio(audio_file) -> dict:
    """
    Transcribe audio to text using locally installed Whisper
    
    Args:
        audio_file: Audio file object (MP3, WAV, M4A, OGG, etc.)
        
    Returns:
        Dictionary with transcribed text
    """
    try:
        if not WHISPER_AVAILABLE:
            print("⚠️ Whisper model not available")
            return {
                "text": "Whisper model not available. Install with: pip install openai-whisper",
                "error": True
            }
        
        # Save uploaded file temporarily
        temp_path = "temp_audio.wav"
        
        try:
            # Read file content
            with open(temp_path, "wb") as f:
                f.write(audio_file.read())
            
            # Transcribe with Whisper
            print(f"🎙️ Transcribing audio...")
            result = model.transcribe(temp_path)
            
            transcribed_text = result["text"]
            print(f"✅ Transcription Complete: {transcribed_text[:100]}...")
            
            return {
                "text": transcribed_text,
                "error": False,
                "source": "Local Whisper"
            }
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        print(f"❌ Transcription error: {str(e)}")
        return {
            "text": f"Error: {str(e)}",
            "error": True
        }


def get_available_models() -> dict:
    """
    Get list of available Whisper models
    
    Returns:
        Dictionary with model info
    """
    models = {
        "tiny": {
            "size": "39M",
            "english_only": False,
            "speed": "Very Fast",
            "accuracy": "Low"
        },
        "base": {
            "size": "140M",
            "english_only": False,
            "speed": "Fast",
            "accuracy": "Medium"
        },
        "small": {
            "size": "466M",
            "english_only": False,
            "speed": "Medium",
            "accuracy": "Good"
        },
        "medium": {
            "size": "1.5G",
            "english_only": False,
            "speed": "Slow",
            "accuracy": "Very Good"
        },
        "large": {
            "size": "2.9G",
            "english_only": False,
            "speed": "Very Slow",
            "accuracy": "Best"
        }
    }
    return models


def change_model(model_name: str) -> dict:
    """
    Change which Whisper model to use
    
    Args:
        model_name: One of "tiny", "base", "small", "medium", "large"
        
    Returns:
        Status dictionary
    """
    global model, WHISPER_AVAILABLE
    
    valid_models = ["tiny", "base", "small", "medium", "large"]
    
    if model_name not in valid_models:
        return {
            "status": "error",
            "message": f"Model must be one of: {valid_models}"
        }
    
    try:
        print(f"📥 Loading Whisper model: {model_name}...")
        model = whisper.load_model(model_name)
        WHISPER_AVAILABLE = True
        print(f"✅ Model '{model_name}' loaded successfully")
        
        return {
            "status": "success",
            "message": f"Switched to model: {model_name}",
            "model": model_name
        }
    except Exception as e:
        WHISPER_AVAILABLE = False
        return {
            "status": "error",
            "message": f"Failed to load model: {str(e)}"
        }