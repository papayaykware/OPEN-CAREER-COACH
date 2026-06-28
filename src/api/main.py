"""
OPEN-CAREER-COACH · src/api/main.py
API REST con FastAPI — v2.0.0-F2

Endpoints:
    GET  /health              → Estado del servicio
    POST /analyze             → Matching explicable completo
    POST /export              → Generación de informes
    GET  /history             → Historial de análisis
    GET  /history/stats       → Estadísticas del historial
    GET  /history/{id}        → Análisis por ID
    GET  /docs                → Documentación automática (Swagger)

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import CVJobMatcher
from src.matching.explainer import MatchingExplainer
from src.exporter.report_exporter import ReportExporter
from src.db.database import Database
from src.db.analysis_repository import AnalysisRepository

from src.api.schemas import (
    AnalyzeRequest, AnalyzeResponse,
    ExportRequest, ExportResponse,
    HealthResponse,
    DimensionScoreResponse, RequirementMatchResponse,
    AnalysisRecordResponse, HistoryResponse, StatsResponse,
)

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open-career-coach")


# ─────────────────────────────────────────────
# ESTADO GLOBAL
# ─────────────────────────────────────────────

class AppState:
    cv_pipeline:  Optional[CVPipeline]         = None
    job_pipeline: Optional[JobPipeline]        = None
    matcher:      Optional[CVJobMatcher]       = None
    explainer:    Optional[MatchingExplainer]  = None
    exporter:     Optional[ReportExporter]     = None
    db:           Optional[Database]           = None
    repository:   Optional[AnalysisRepository] = None
    ready:        bool                         = False


app_state = AppState()


# ─────────────────────────────────────────────
# LIFESPAN
# ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando pipelines...")
    try:
        app_state.cv_pipeline  = CVPipeline()
        app_state.job_pipeline = JobPipeline()
        app_state.matcher      = CVJobMatcher()
        app_state.explainer    = MatchingExplainer()
        app_state.exporter     = ReportExporter()
        app_state.db           = Database()
        app_state.repository   = AnalysisRepository(app_state.db)
        app_state.ready        = True
        logger.info("Pipelines listos.")
    except Exception as e:
        logger.error(f"Error al inicializar pipelines: {e}")
        app_state.ready = False
    yield
    logger.info("Apagando servicio.")


# ─────────────────────────────────────────────
# APLICACIÓN
# ─────────────────────────────────────────────

app = FastAPI(
    title="OPEN-CAREER-COACH API",
    description=(
        "API REST para análisis de matching CV-oferta con explicabilidad. "
        "Autor conceptual: Claude (Anthropic) · Director: Javi Ciborro (@papayaykware)"
    ),
    version="2.0.0",
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def _nivel(score: float) -> str:
    if score >= 0.65:
        return "alto"
    elif score >= 0.40:
        return "moderado"
    return "bajo"


def _check_ready():
    if not app_state.ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio no está listo. Los pipelines no se inicializaron correctamente."
        )


def _record_to_response(rec) -> AnalysisRecordResponse:
    return AnalysisRecordResponse(
        id=rec.id,
        created_at=rec.created_at,
        global_score=rec.global_score,
        nivel=rec.nivel,
        narrative=rec.narrative,
        strengths=rec.strengths,
        gaps=rec.gaps,
        dimension_scores=[DimensionScoreResponse(**ds) for ds in rec.dimension_scores],
        gap_analysis=[RequirementMatchResponse(**rm) for rm in rec.gap_analysis],
        metadata=rec.metadata,
        profile_type=rec.profile_type,
        export_md=rec.export_md,
        export_json=rec.export_json,
    )


# ─────────────────────────────────────────────
# ENDPOINTS — SISTEMA
# ─────────────────────────────────────────────

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado del servicio",
    tags=["Sistema"],
)
async def health():
    """Devuelve el estado de los pipelines y la versión del servicio."""
    return HealthResponse(
        status="ok" if app_state.ready else "degraded",
        version="2.0.0",
        pipelines={
            "cv_pipeline":  "ok" if app_state.cv_pipeline  else "error",
            "job_pipeline": "ok" if app_state.job_pipeline else "error",
            "matcher":      "ok" if app_state.matcher      else "error",
            "explainer":    "ok" if app_state.explainer    else "error",
            "exporter":     "ok" if app_state.exporter     else "error",
            "database":     "ok" if app_state.db           else "error",
        }
    )


# ─────────────────────────────────────────────
# ENDPOINTS — MATCHING
# ─────────────────────────────────────────────

@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Análisis de matching CV-oferta",
    tags=["Matching"],
    status_code=status.HTTP_200_OK,
)
async def analyze(request: AnalyzeRequest):
    """
    Ejecuta el pipeline completo de matching explicable y persiste
    el resultado en SQLite.
    """
    _check_ready()
    try:
        cv_data  = app_state.cv_pipeline.process_text(request.cv_text)
        job_data = app_state.job_pipeline.process(request.offer_text)

        base = app_state.matcher.calculate_match(
            cv_data=cv_data.__dict__,
            job_data=job_data.__dict__,
        )
        explained = app_state.explainer.explain(
            request.cv_text,
            request.offer_text,
            profile_type=request.profile_type,
        )

        export_paths = None
        if request.export_formats:
            rutas = app_state.exporter.export(
                explained, base, formatos=request.export_formats
            )
            export_paths = {k: str(v) for k, v in rutas.items()}

        # Persistir en SQLite
        app_state.repository.save(
            result=explained,
            cv_text=request.cv_text,
            offer_text=request.offer_text,
            nivel=_nivel(explained.global_score),
            export_paths=export_paths,
        )

        return AnalyzeResponse(
            global_score=explained.global_score,
            nivel=_nivel(explained.global_score),
            narrative=explained.narrative,
            strengths=explained.strengths,
            gaps=explained.gaps,
            dimension_scores=[
                DimensionScoreResponse(
                    dimension=ds.dimension,
                    score=ds.score,
                    weight=ds.weight,
                    cv_fragments=ds.cv_fragments,
                    offer_fragments=ds.offer_fragments,
                )
                for ds in explained.dimension_scores
            ],
            gap_analysis=[
                RequirementMatchResponse(
                    requirement=rm.requirement,
                    status=rm.status,
                    confidence=rm.confidence,
                    cv_evidence=rm.cv_evidence,
                )
                for rm in explained.gap_analysis
            ],
            export_paths=export_paths,
            metadata={
                **explained.metadata,
                "base_score":          base.global_score,
                "semantic_similarity": base.semantic_similarity,
                "skill_match_score":   base.skill_match_score,
                "matched_skills":      list(base.matched_skills),
                "missing_skills":      list(base.missing_skills),
                "recommendations":     list(base.recommendations),
            }
        )

    except Exception as e:
        logger.error(f"Error en /analyze: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el análisis: {str(e)}"
        )


# ─────────────────────────────────────────────
# ENDPOINTS — EXPORTACIÓN
# ─────────────────────────────────────────────

@app.post(
    "/export",
    response_model=ExportResponse,
    summary="Exportación de informes",
    tags=["Exportación"],
    status_code=status.HTTP_200_OK,
)
async def export(request: ExportRequest):
    """Genera informes en los formatos solicitados y devuelve las rutas."""
    _check_ready()
    try:
        cv_data  = app_state.cv_pipeline.process_text(request.cv_text)
        job_data = app_state.job_pipeline.process(request.offer_text)
        base     = app_state.matcher.calculate_match(
            cv_data=cv_data.__dict__,
            job_data=job_data.__dict__,
        )
        explained = app_state.explainer.explain(request.cv_text, request.offer_text)
        rutas = app_state.exporter.export(
            explained, base,
            nombre_base=request.nombre_base,
            formatos=request.formatos,
        )
        return ExportResponse(
            paths={k: str(v) for k, v in rutas.items()},
            message=f"Informe generado correctamente en {len(rutas)} formato(s)."
        )
    except Exception as e:
        logger.error(f"Error en /export: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la exportación: {str(e)}"
        )


# ─────────────────────────────────────────────
# ENDPOINTS — HISTORIAL
# ─────────────────────────────────────────────

@app.get(
    "/history/stats",
    response_model=StatsResponse,
    summary="Estadísticas del historial",
    tags=["Historial"],
)
async def history_stats():
    """Devuelve estadísticas agregadas de todos los análisis almacenados."""
    _check_ready()
    s = app_state.repository.stats()
    return StatsResponse(
        total=s.get("total", 0),
        avg_score=s.get("avg_score"),
        max_score=s.get("max_score"),
        min_score=s.get("min_score"),
        total_alto=s.get("total_alto", 0),
        total_moderado=s.get("total_moderado", 0),
        total_bajo=s.get("total_bajo", 0),
    )


@app.get(
    "/history",
    response_model=HistoryResponse,
    summary="Historial de análisis",
    tags=["Historial"],
)
async def history(
    limit: int = 20,
    offset: int = 0,
    min_score: Optional[float] = None,
    nivel: Optional[str] = None,
):
    """Lista los análisis almacenados con filtros opcionales y paginación."""
    _check_ready()
    records = app_state.repository.list_recent(
        limit=limit, offset=offset, min_score=min_score, nivel=nivel
    )
    total = app_state.repository.count()
    return HistoryResponse(
        total=total,
        limit=limit,
        offset=offset,
        records=[_record_to_response(r) for r in records],
    )


@app.get(
    "/history/{analysis_id}",
    response_model=AnalysisRecordResponse,
    summary="Recuperar análisis por ID",
    tags=["Historial"],
)
async def get_analysis(analysis_id: int):
    """Recupera un análisis concreto por su ID."""
    _check_ready()
    rec = app_state.repository.get_by_id(analysis_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe ningún análisis con ID {analysis_id}."
        )
    return _record_to_response(rec)
