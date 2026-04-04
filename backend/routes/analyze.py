"""
API routes for code analysis endpoints.
"""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import AnalysisRequest, AnalysisResponse, HealthResponse
from backend.services.analyzer import get_analyzer_service
from backend.services.llm_service import get_llm_service
from backend.config import settings

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze source code for security vulnerabilities.
    
    This endpoint performs comprehensive security analysis using:
    - Static analysis for pattern-based vulnerability detection
    - LLM analysis for semantic understanding and complex vulnerabilities
    
    Returns attack surfaces, trust boundaries, vulnerabilities, and fix suggestions.
    """
    if not request.code or not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if len(request.code) > settings.max_code_length:
        raise HTTPException(
            status_code=400, 
            detail=f"Code exceeds maximum length of {settings.max_code_length} characters"
        )
    
    analyzer = get_analyzer_service()
    result = await analyzer.analyze_code(
        code=request.code,
        language=request.language or "auto",
        context=request.context
    )
    
    return result


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check the health status of the analyzer service.
    
    Returns the current status, LLM mode, and version information.
    """
    llm_service = get_llm_service()
    is_healthy = llm_service.health_check()
    
    return HealthResponse(
        status="healthy" if is_healthy else "degraded",
        llm_mode=settings.llm_mode,
        version="1.0.0"
    )


@router.get("/config")
async def get_config():
    """
    Get current configuration (non-sensitive values only).
    """
    return {
        "llm_mode": settings.llm_mode,
        "model": settings.openai_model if settings.llm_mode == "online" else settings.ollama_model,
        "max_code_length": settings.max_code_length,
        "analysis_timeout": settings.analysis_timeout
    }
