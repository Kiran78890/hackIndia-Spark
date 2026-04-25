from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routes.verify import router as verify_router
from routes.score import router as score_router
from routes.voice import router as voice_router
from core.config import settings

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="🔍 Fake News Detector API",
    description="AI-powered fake news detection system with multi-language support",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(verify_router, prefix="/api", tags=["verification"])
app.include_router(score_router, prefix="/api", tags=["scoring"])
app.include_router(voice_router, prefix="/api", tags=["voice"])

# Health check endpoint
@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "🔍 Fake News Detector API v2.0 is running!",
        "status": "healthy",
        "features": [
            "✅ Multi-language support",
            "✅ Google Gemini AI analysis",
            "✅ Fact Check API verification",
            "✅ Local Whisper audio transcription",
            "✅ Hugging Face classification"
        ],
        "scoring": {
            "ai_analysis": "70%",
            "fact_check": "30%"
        },
        "endpoints": {
            "verify_text": "/api/verify/text (POST)",
            "verify_voice": "/api/voice/verify (POST)",
            "transcribe": "/api/voice/transcribe (POST)",
            "calculate_score": "/api/score/calculate (POST)",
            "get_verdict": "/api/score/verdict/{score} (GET)",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "apis": {
            "gemini": "✅" if settings.GOOGLE_GEMINI_API_KEY else "❌",
            "factcheck": "✅" if settings.FACT_CHECK_API_KEY else "❌",
            "huggingface": "✅" if settings.HUGGINGFACE_API_KEY else "❌",
            "whisper": "✅ (Local)"
        },
        "note": "News API integration removed"
    }

# Run app
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Fake News Detector API v2.0...")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("❤️ Health: http://localhost:8000/health")
    print("⚙️ Scoring: 70% AI + 30% Fact-Check")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)