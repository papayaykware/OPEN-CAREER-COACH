"""
OPEN-CAREER-COACH · src/db/analysis_repository.py
Repositorio de análisis — v2.0.0

CRUD completo sobre la tabla analyses.

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional

from src.db.database import Database
from src.matching.explainer import ExplainedMatchResult

logger = logging.getLogger("open-career-coach.repository")


# ─────────────────────────────────────────────
# DATACLASS DE SALIDA
# ─────────────────────────────────────────────

@dataclass
class AnalysisRecord:
    """Registro de análisis tal como se almacena en SQLite."""
    id: int
    created_at: str
    cv_text: str
    offer_text: str
    global_score: float
    nivel: str
    narrative: str
    strengths: list[str]
    gaps: list[str]
    dimension_scores: list[dict]
    gap_analysis: list[dict]
    metadata: dict
    profile_type: Optional[str]
    export_md: Optional[str]
    export_json: Optional[str]

    @classmethod
    def from_row(cls, row) -> "AnalysisRecord":
        return cls(
            id=row["id"],
            created_at=row["created_at"],
            cv_text=row["cv_text"],
            offer_text=row["offer_text"],
            global_score=row["global_score"],
            nivel=row["nivel"],
            narrative=row["narrative"],
            strengths=json.loads(row["strengths"]),
            gaps=json.loads(row["gaps"]),
            dimension_scores=json.loads(row["dimension_scores"]),
            gap_analysis=json.loads(row["gap_analysis"]),
            metadata=json.loads(row["metadata"]),
            profile_type=row["profile_type"],
            export_md=row["export_md"],
            export_json=row["export_json"],
        )


# ─────────────────────────────────────────────
# REPOSITORIO
# ─────────────────────────────────────────────

class AnalysisRepository:
    """
    CRUD sobre la tabla analyses.

    Uso:
        db   = Database()
        repo = AnalysisRepository(db)
        id_  = repo.save(result, cv_text, offer_text)
        rec  = repo.get_by_id(id_)
        recs = repo.list_recent(limit=10)
    """

    def __init__(self, db: Database):
        self.db = db

    # ── Escritura ─────────────────────────────────────────────────────────

    def save(
        self,
        result: ExplainedMatchResult,
        cv_text: str,
        offer_text: str,
        nivel: str,
        export_paths: Optional[dict[str, str]] = None,
    ) -> int:
        """
        Persiste un ExplainedMatchResult y devuelve el ID generado.

        Args:
            result:       Resultado del MatchingExplainer.
            cv_text:      Texto del CV analizado.
            offer_text:   Texto de la oferta analizada.
            nivel:        Nivel de encaje ('alto' | 'moderado' | 'bajo').
            export_paths: Rutas de los informes exportados (opcional).

        Returns:
            ID del registro insertado.
        """
        sql = """
            INSERT INTO analyses (
                cv_text, offer_text, global_score, nivel, narrative,
                strengths, gaps, dimension_scores, gap_analysis,
                metadata, profile_type, export_md, export_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            cv_text,
            offer_text,
            result.global_score,
            nivel,
            result.narrative,
            json.dumps(result.strengths, ensure_ascii=False),
            json.dumps(result.gaps, ensure_ascii=False),
            json.dumps(
                [
                    {
                        "dimension":       ds.dimension,
                        "score":           ds.score,
                        "weight":          ds.weight,
                        "cv_fragments":    ds.cv_fragments,
                        "offer_fragments": ds.offer_fragments,
                    }
                    for ds in result.dimension_scores
                ],
                ensure_ascii=False,
            ),
            json.dumps(
                [
                    {
                        "requirement": rm.requirement,
                        "status":      rm.status,
                        "confidence":  rm.confidence,
                        "cv_evidence": rm.cv_evidence,
                    }
                    for rm in result.gap_analysis
                ],
                ensure_ascii=False,
            ),
            json.dumps(result.metadata, ensure_ascii=False),
            result.metadata.get("profile_type"),
            export_paths.get("md")   if export_paths else None,
            export_paths.get("json") if export_paths else None,
        )

        with self.db.connection() as conn:
            cursor = conn.execute(sql, params)
            record_id = cursor.lastrowid
            logger.info(f"Análisis guardado con ID {record_id} (score={result.global_score:.2f})")
            return record_id

    # ── Lectura ───────────────────────────────────────────────────────────

    def get_by_id(self, analysis_id: int) -> Optional[AnalysisRecord]:
        """Recupera un análisis por ID. Devuelve None si no existe."""
        sql = "SELECT * FROM analyses WHERE id = ?"
        with self.db.connection() as conn:
            row = conn.execute(sql, (analysis_id,)).fetchone()
        return AnalysisRecord.from_row(row) if row else None

    def list_recent(
        self,
        limit: int = 20,
        offset: int = 0,
        min_score: Optional[float] = None,
        nivel: Optional[str] = None,
    ) -> list[AnalysisRecord]:
        """
        Lista análisis recientes con filtros opcionales.

        Args:
            limit:     Máximo de registros a devolver.
            offset:    Desplazamiento para paginación.
            min_score: Filtra por score mínimo (0.0 – 1.0).
            nivel:     Filtra por nivel ('alto' | 'moderado' | 'bajo').

        Returns:
            Lista de AnalysisRecord ordenada por fecha descendente.
        """
        conditions = []
        params: list = []

        if min_score is not None:
            conditions.append("global_score >= ?")
            params.append(min_score)
        if nivel:
            conditions.append("nivel = ?")
            params.append(nivel)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"""
            SELECT * FROM analyses
            {where}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        params += [limit, offset]

        with self.db.connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [AnalysisRecord.from_row(r) for r in rows]

    def count(self) -> int:
        """Número total de análisis almacenados."""
        with self.db.connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]

    def stats(self) -> dict:
        """Estadísticas agregadas del historial."""
        sql = """
            SELECT
                COUNT(*)                    AS total,
                ROUND(AVG(global_score), 4) AS avg_score,
                ROUND(MAX(global_score), 4) AS max_score,
                ROUND(MIN(global_score), 4) AS min_score,
                SUM(CASE WHEN nivel = 'alto'     THEN 1 ELSE 0 END) AS total_alto,
                SUM(CASE WHEN nivel = 'moderado' THEN 1 ELSE 0 END) AS total_moderado,
                SUM(CASE WHEN nivel = 'bajo'     THEN 1 ELSE 0 END) AS total_bajo
            FROM analyses
        """
        with self.db.connection() as conn:
            row = conn.execute(sql).fetchone()
        return dict(row) if row else {}

    # ── Eliminación ───────────────────────────────────────────────────────

    def delete(self, analysis_id: int) -> bool:
        """Elimina un análisis por ID. Devuelve True si existía."""
        with self.db.connection() as conn:
            cursor = conn.execute(
                "DELETE FROM analyses WHERE id = ?", (analysis_id,)
            )
        return cursor.rowcount > 0
