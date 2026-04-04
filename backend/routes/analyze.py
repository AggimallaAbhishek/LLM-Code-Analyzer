"""
API routes for code analysis endpoints.
"""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    AnalysisRequest, AnalysisResponse, HealthResponse,
    MultiFileAnalysisRequest, MultiFileAnalysisResponse, FileAnalysisResult
)
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


@router.post("/analyze-multiple", response_model=MultiFileAnalysisResponse)
async def analyze_multiple_files(request: MultiFileAnalysisRequest) -> MultiFileAnalysisResponse:
    """
    Analyze multiple files for security vulnerabilities.
    
    This endpoint analyzes a batch of files and returns aggregated results.
    Each file is analyzed independently, and results are combined.
    """
    if not request.files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(request.files) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 files allowed per request")
    
    analyzer = get_analyzer_service()
    results = []
    total_vulnerabilities = 0
    risk_scores = []
    
    for file_info in request.files:
        filename = file_info.get('filename', 'unknown')
        content = file_info.get('content', '')
        language = file_info.get('language', 'auto')
        
        if not content.strip():
            continue
            
        if len(content) > settings.max_code_length:
            # Skip files that are too large but note them
            results.append(FileAnalysisResult(
                filename=filename,
                filepath=filename,
                analysis=AnalysisResponse(
                    success=False,
                    language=language,
                    summary=f"File skipped: exceeds maximum length of {settings.max_code_length} characters",
                    risk_score=0,
                    error="File too large"
                )
            ))
            continue
        
        try:
            analysis = await analyzer.analyze_code(
                code=content,
                language=language,
                context=f"File: {filename}"
            )
            results.append(FileAnalysisResult(
                filename=filename,
                filepath=filename,
                analysis=analysis
            ))
            total_vulnerabilities += len(analysis.vulnerabilities)
            if analysis.risk_score > 0:
                risk_scores.append(analysis.risk_score)
        except Exception as e:
            results.append(FileAnalysisResult(
                filename=filename,
                filepath=filename,
                analysis=AnalysisResponse(
                    success=False,
                    language=language,
                    summary=f"Analysis failed: {str(e)}",
                    risk_score=0,
                    error=str(e)
                )
            ))
    
    overall_risk = int(sum(risk_scores) / len(risk_scores)) if risk_scores else 0
    
    return MultiFileAnalysisResponse(
        success=True,
        total_files=len(results),
        total_vulnerabilities=total_vulnerabilities,
        overall_risk_score=overall_risk,
        summary=f"Analyzed {len(results)} files. Found {total_vulnerabilities} vulnerabilities. Overall risk: {overall_risk}/100.",
        results=results
    )
