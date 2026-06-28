"""
OPEN-CAREER-COACH · src/api/main.py
API REST con FastAPI — v2.0.0

Endpoints:
    GET  /health          → Estado del servicio
    POST /analyze         → Matching explicable completo
    POST /export          → Generación de informes
    GET  /docs            → Documentación automática (Swagger)

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

from src.api.schemas import (
    AnalyzeRequest, AnalyzeResponse,
    ExportRequest, ExportResponse,
    HealthResponse,
    DimensionScoreResponse, RequirementMatchResponse,
)

from src.db.database import Database
from src.db.analysis_repository import AnalysisRepository

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open-career-coach")


# ─────────────────────────────────────────────
# ESTADO GLOBAL (inicialización en startup)
# ─────────────────────────────────────────────

class AppState:
    cv_pipeline:  Optional[CVPipeline]  = None
    job_pipeline: Optional[JobPipeline] = None
    matcher:      Optional[CVJobMatcher]    = None
    explainer:    Optional[MatchingExplainer] = None
    exporter:     Optional[ReportExporter]    = None
    ready: bool = False


app_state = AppState()

db:         Optional[Database]            = None
repository: Optional[AnalysisRepository] = None

# ─────────────────────────────────────────────
# LIFESPAN — carga de pipelines al arranque
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
        app_state.db         = Database()
app_state.repository = AnalysisRepository(app_state.db)
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
    allow_origins=["*"],        # ajustar en producción
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


# ─────────────────────────────────────────────
# ENDPOINTS
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
        }
    )


@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Análisis de matching CV-oferta",
    tags=["Matching"],
    status_code=status.HTTP_200_OK,
)
async def analyze(request: AnalyzeRequest):
    """
    Ejecuta el pipeline completo de matching explicable:

    - Parsing de CV y oferta
    - Matching base (embeddings + similitud coseno)
    - Matching explicable (dimensional + gap analysis + narrativa)
    - Exportación opcional de informes

    Devuelve un resultado estructurado con score, dimensiones,
    gap analysis y narrativa en lenguaje natural.
    """
    _check_ready()

    try:
        # Parsing
        cv_data  = app_state.cv_pipeline.process_text(request.cv_text)
        job_data = app_state.job_pipeline.process(request.offer_text)

        # Matching base
        base = app_state.matcher.calculate_match(
            cv_data=cv_data.__dict__,
            job_data=job_data.__dict__,
        )

        # Matching explicable
        explained = app_state.explainer.explain(
            request.cv_text,
            request.offer_text,
            profile_type=request.profile_type,
        )

        # Exportación opcional
        export_paths = None
        if request.export_formats:
            rutas = app_state.exporter.export(
                explained,
                base,
                formatos=request.export_formats,
            )
            export_paths = {k: str(v) for k, v in rutas.items()}

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
                "base_score":            base.global_score,
                "semantic_similarity":   base.semantic_similarity,
                "skill_match_score":     base.skill_match_score,
                "matched_skills":        list(base.matched_skills),
                "missing_skills":        list(base.missing_skills),
                "recommendations":       list(base.recommendations),
            }
        )

    except Exception as e:
        logger.error(f"Error en /analyze: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el análisis: {str(e)}"
        )


@app.post(
    "/export",
    response_model=ExportResponse,
    summary="Exportación de informes",
    tags=["Exportación"],
    status_code=status.HTTP_200_OK,
)
async def export(request: ExportRequest):
    """
    Genera informes en los formatos solicitados (Markdown y/o JSON)
    y devuelve las rutas de los archivos generados.
    """
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
            explained,
            base,
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
