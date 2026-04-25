from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from pathlib import Path
from routes.verify import router as verify_router
from routes.score import router as score_router
from routes.voice import router as voice_router
from core.config import settings

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

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(verify_router)
app.include_router(score_router)
app.include_router(voice_router)

# Path to client directory
CLIENT_DIR = Path(__file__).parent.parent / "client"

# Mount static files (images, CSS, fonts)
if (CLIENT_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=CLIENT_DIR / "assets"), name="assets")

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
        }
    }

# Serve static files for known file types
@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files"""
    # List of file extensions to serve directly
    static_extensions = [
        '.html', '.css', '.js', '.json',
        '.png', '.jpg', '.jpeg', '.gif', '.svg',
        '.woff', '.woff2', '.ttf', '.otf',
        '.mp3', '.wav', '.webm'
    ]
    
    file_full_path = CLIENT_DIR / file_path
    
    # If file exists and has static extension, serve it
    if file_full_path.exists() and file_full_path.is_file():
        for ext in static_extensions:
            if file_path.endswith(ext):
                return FileResponse(file_full_path)
    
    # Default: serve index.html for SPA routing
    index_path = CLIENT_DIR / "HACKINDIA.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    
    return {"error": "File not found", "requested": file_path}

# Run app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print("🚀 Starting Fake News Detector API v2.0...")
    print(f"📍 Frontend: http://localhost:{port}")
    print(f"📍 Server: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"❤️ Health: http://localhost:{port}/health")
    print("⚙️ Scoring: 70% AI + 30% Fact-Check")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)