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
    title="LLM Code Analyzer",
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


@app.get("/")
async def root():
    """Serve the frontend or return API info."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {
        "name": "LLM Code Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 LLM Code Analyzer starting...")
    print(f"📊 Mode: {settings.llm_mode}")
    print(f"🤖 Model: {settings.openai_model if settings.llm_mode == 'online' else settings.ollama_model}")
    print(f"📖 API docs available at: http://{settings.host}:{settings.port}/docs")


# Mount static files if frontend exists
frontend_static = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")
if os.path.exists(frontend_static):
    app.mount("/static", StaticFiles(directory=frontend_static), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
