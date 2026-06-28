"""
OPEN-CAREER-COACH · src/api/schemas.py
Modelos Pydantic para la API REST — v2.0.0

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


# ─────────────────────────────────────────────
# REQUESTS
# ─────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    cv_text: str = Field(
        ...,
        min_length=50,
        description="Texto completo del CV (mínimo 50 caracteres)."
    )
    offer_text: str = Field(
        ...,
        min_length=50,
        description="Texto completo de la oferta de empleo."
    )
    profile_type: Optional[str] = Field(
        None,
        description="Tipo de perfil para ajuste de pesos (opcional)."
    )
    export_formats: Optional[list[str]] = Field(
        None,
        description="Formatos de exportación: ['md', 'json']. Si se omite, no exporta."
    )


class ExportRequest(BaseModel):
    cv_text: str = Field(..., min_length=50)
    offer_text: str = Field(..., min_length=50)
    nombre_base: str = Field("informe_matching", description="Nombre base del archivo.")
    formatos: list[str] = Field(["md", "json"], description="Formatos a generar.")


# ─────────────────────────────────────────────
# RESPONSES
# ─────────────────────────────────────────────

class DimensionScoreResponse(BaseModel):
    dimension: str
    score: float
    weight: float
    cv_fragments: list[str]
    offer_fragments: list[str]


class RequirementMatchResponse(BaseModel):
    requirement: str
    status: str        # "cubierto" | "parcial" | "ausente"
    confidence: float
    cv_evidence: Optional[str]


class AnalyzeResponse(BaseModel):
    global_score: float
    nivel: str         # "alto" | "moderado" | "bajo"
    narrative: str
    strengths: list[str]
    gaps: list[str]
    dimension_scores: list[DimensionScoreResponse]
    gap_analysis: list[RequirementMatchResponse]
    export_paths: Optional[dict[str, str]] = None
    metadata: dict


class ExportResponse(BaseModel):
    paths: dict[str, str]
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str
    pipelines: dict[str, str]

# ── Schemas de historial (v2.0.0-F2) ─────────────────────────────────────

class AnalysisRecordResponse(BaseModel):
    id: int
    created_at: str
    global_score: float
    nivel: str
    narrative: str
    strengths: list[str]
    gaps: list[str]
    dimension_scores: list[DimensionScoreResponse]
    gap_analysis: list[RequirementMatchResponse]
    metadata: dict
    profile_type: Optional[str]
    export_md: Optional[str]
    export_json: Optional[str]


class HistoryResponse(BaseModel):
    total: int
    limit: int
    offset: int
    records: list[AnalysisRecordResponse]


class StatsResponse(BaseModel):
    total: int
    avg_score: Optional[float]
    max_score: Optional[float]
    min_score: Optional[float]
    total_alto: int
    total_moderado: int
    total_bajo: int
