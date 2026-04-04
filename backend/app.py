"""
LLM Code Analyzer - FastAPI Application

A security-focused code analysis tool that combines LLM intelligence
with static analysis to identify vulnerabilities and suggest fixes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.routes.analyze import router as analyze_router
from backend.config import settings

# Create FastAPI application
app = FastAPI(
    title="SecureCodeAI",
    description="AI-powered code security analysis tool",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(analyze_router, prefix="/api", tags=["analysis"])

# Check for built React frontend
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
frontend_assets = os.path.join(frontend_dist, "assets")

if os.path.exists(frontend_dist):
    # Serve static assets from React build
    if os.path.exists(frontend_assets):
        app.mount("/assets", StaticFiles(directory=frontend_assets), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve React SPA - all routes go to index.html"""
        # Don't serve API routes or docs
        if full_path.startswith("api/") or full_path in ["docs", "redoc", "openapi.json"]:
            return None
        
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Fallback to index.html for SPA routing
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        """Return API info when frontend is not built."""
        return {
            "name": "SecureCodeAI API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health",
            "note": "Run 'npm run build' in frontend/ to enable the web UI"
        }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 SecureCodeAI starting...")
    print(f"📊 Mode: {settings.llm_mode}")
    if settings.llm_mode == "openai":
        print(f"🤖 Model: {settings.openai_model}")
    elif settings.llm_mode == "gemini":
        print(f"🤖 Model: {settings.gemini_model}")
    else:
        print(f"🤖 Model: {settings.ollama_model}")
    print(f"📖 API docs available at: http://{settings.host}:{settings.port}/docs")
    if os.path.exists(frontend_dist):
        print(f"🌐 Frontend available at: http://{settings.host}:{settings.port}/")
    else:
        print(f"⚠️  Frontend not built. Run 'cd frontend && npm run build'")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
