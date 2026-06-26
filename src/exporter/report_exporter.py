"""
OPEN-CAREER-COACH · src/exporter/report_exporter.py
Exportación de informes — v1.1.0

Formatos soportados: Markdown (.md) · JSON (.json)

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.matching.explainer import ExplainedMatchResult


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────

DEFAULT_OUTPUT_DIR = Path("reports")
TIMESTAMP_FORMAT   = "%Y%m%d_%H%M%S"


# ─────────────────────────────────────────────
# EXPORTADOR PRINCIPAL
# ─────────────────────────────────────────────

class ReportExporter:
    """
    Genera informes de matching en Markdown y JSON a partir de
    un ExplainedMatchResult producido por MatchingExplainer.

    Uso:
        exporter = ReportExporter()
        paths = exporter.export(result, base_result, "informe_analisis")
        print(paths)   # {'md': PosixPath(...), 'json': PosixPath(...)}
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Markdown ──────────────────────────────────────────────────────────

    def to_markdown(
        self,
        result: ExplainedMatchResult,
        base_result=None,
        titulo: str = "Informe de Matching",
    ) -> str:
        """Genera el informe completo en formato Markdown."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        score_pct = int(result.global_score * 100)

        nivel, emoji = self._nivel(result.global_score)

        lines = [
            f"# {emoji} {titulo}",
            f"",
            f"> Generado el {ts} · Open Career Coach v1.1.0",
            f"> Autor conceptual: Claude (Anthropic) · Director: Javi Ciborro (@papayaykware)",
            f"",
            f"---",
            f"",
            f"## 📊 Resumen Ejecutivo",
            f"",
            f"| Métrica | Valor |",
            f"|---------|-------|",
            f"| **Nivel de encaje** | {emoji} {nivel} |",
            f"| **Score explicable** | {score_pct}% |",
        ]

        if base_result:
            lines += [
                f"| **Score base (embeddings)** | {base_result.global_score:.2f} |",
                f"| **Similitud semántica** | {base_result.semantic_similarity:.2f} |",
                f"| **Match de skills** | {base_result.skill_match_score:.2f} |",
            ]

        lines += [
            f"",
            f"### Narrativa",
            f"",
            result.narrative,
            f"",
            f"---",
            f"",
            f"## 📐 Desglose Dimensional",
            f"",
            f"| Dimensión | Score | Peso | Barra |",
            f"|-----------|-------|------|-------|",
        ]

        for ds in result.dimension_scores:
            barra = self._barra(ds.score)
            nombre = ds.dimension.replace("_", " ").title()
            lines.append(
                f"| {nombre} | {int(ds.score*100)}% | {int(ds.weight*100)}% | {barra} |"
            )

        lines += [
            f"",
            f"### Términos detectados por dimensión",
            f"",
        ]

        for ds in result.dimension_scores:
            nombre = ds.dimension.replace("_", " ").title()
            cv_terms   = ", ".join(ds.cv_fragments[:8])  or "—"
            ofr_terms  = ", ".join(ds.offer_fragments[:8]) or "—"
            lines += [
                f"**{nombre}**",
                f"- CV: `{cv_terms}`",
                f"- Oferta: `{ofr_terms}`",
                f"",
            ]

        lines += [
            f"---",
            f"",
            f"## 🔎 Gap Analysis por Requisito",
            f"",
        ]

        cubiertos = [r for r in result.gap_analysis if r.status == "cubierto"]
        parciales = [r for r in result.gap_analysis if r.status == "parcial"]
        ausentes  = [r for r in result.gap_analysis if r.status == "ausente"]

        for seccion, items, icono in [
            ("Requisitos cubiertos",            cubiertos, "✅"),
            ("Requisitos parcialmente cubiertos", parciales, "🔶"),
            ("Requisitos no cubiertos",          ausentes,  "❌"),
        ]:
            if items:
                lines.append(f"### {icono} {seccion} ({len(items)})")
                lines.append("")
                for rm in items:
                    evidencia = f" · *evidencia: {rm.cv_evidence}*" if rm.cv_evidence else ""
                    lines.append(f"- {rm.requirement[:120]}{evidencia}")
                lines.append("")

        if base_result:
            lines += [
                f"---",
                f"",
                f"## 🛠️ Skills — Motor Base",
                f"",
                f"**Skills coincidentes:** {', '.join(base_result.matched_skills) or '—'}",
                f"",
                f"**Skills faltantes:** {', '.join(base_result.missing_skills) or '—'}",
                f"",
                f"**Recomendaciones:**",
                f"",
            ]
            for rec in base_result.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        lines += [
            f"---",
            f"",
            f"*Informe generado por Open Career Coach v1.1.0 · Licencia MIT*",
            f"*github.com/papayaykware/OPEN-CAREER-COACH*",
        ]

        return "\n".join(lines)

    # ── JSON ──────────────────────────────────────────────────────────────

    def to_json(
        self,
        result: ExplainedMatchResult,
        base_result=None,
        titulo: str = "Informe de Matching",
    ) -> str:
        """Serializa el resultado completo a JSON estructurado."""
        payload = {
            "meta": {
                "titulo": titulo,
                "timestamp": datetime.now().isoformat(),
                "version": "1.1.0",
                "proyecto": "OPEN-CAREER-COACH",
                "autor_conceptual": "Claude (Anthropic)",
                "director": "Javi Ciborro (@papayaykware)",
            },
            "explained_result": {
                "global_score": result.global_score,
                "nivel": self._nivel(result.global_score)[0],
                "narrative": result.narrative,
                "strengths": result.strengths,
                "gaps": result.gaps,
                "dimension_scores": [
                    {
                        "dimension":       ds.dimension,
                        "score":           ds.score,
                        "weight":          ds.weight,
                        "cv_fragments":    ds.cv_fragments,
                        "offer_fragments": ds.offer_fragments,
                    }
                    for ds in result.dimension_scores
                ],
                "gap_analysis": [
                    {
                        "requirement": rm.requirement,
                        "status":      rm.status,
                        "confidence":  rm.confidence,
                        "cv_evidence": rm.cv_evidence,
                    }
                    for rm in result.gap_analysis
                ],
                "metadata": result.metadata,
            },
        }

        if base_result:
            payload["base_result"] = {
                "global_score":          base_result.global_score,
                "semantic_similarity":   base_result.semantic_similarity,
                "skill_match_score":     base_result.skill_match_score,
                "experience_match_score": base_result.experience_match_score,
                "matched_skills":        list(base_result.matched_skills),
                "missing_skills":        list(base_result.missing_skills),
                "recommendations":       list(base_result.recommendations),
            }

        return json.dumps(payload, ensure_ascii=False, indent=2)

    # ── Escritura a disco ─────────────────────────────────────────────────

    def export(
        self,
        result: ExplainedMatchResult,
        base_result=None,
        nombre_base: str = "informe",
        formatos: Optional[list[str]] = None,
        titulo: str = "Informe de Matching",
    ) -> dict[str, Path]:
        """
        Escribe los informes en disco y devuelve un dict con las rutas.

        Args:
            result:      ExplainedMatchResult del MatchingExplainer.
            base_result: Resultado del CVJobMatcher (opcional).
            nombre_base: Nombre base del archivo (sin extensión).
            formatos:    Lista de formatos a generar. Default: ['md', 'json'].
            titulo:      Título del informe.

        Returns:
            {'md': Path(...), 'json': Path(...)}  según formatos solicitados.
        """
        if formatos is None:
            formatos = ["md", "json"]

        ts = datetime.now().strftime(TIMESTAMP_FORMAT)
        stem = f"{nombre_base}_{ts}"
        rutas: dict[str, Path] = {}

        if "md" in formatos:
            contenido = self.to_markdown(result, base_result, titulo)
            ruta = self.output_dir / f"{stem}.md"
            ruta.write_text(contenido, encoding="utf-8")
            rutas["md"] = ruta

        if "json" in formatos:
            contenido = self.to_json(result, base_result, titulo)
            ruta = self.output_dir / f"{stem}.json"
            ruta.write_text(contenido, encoding="utf-8")
            rutas["json"] = ruta

        return rutas

    # ── Utilidades internas ───────────────────────────────────────────────

    @staticmethod
    def _nivel(score: float) -> tuple[str, str]:
        if score >= 0.65:
            return "Alto encaje", "🟢"
        elif score >= 0.40:
            return "Encaje moderado", "🟡"
        return "Encaje bajo", "🔴"

    @staticmethod
    def _barra(score: float, longitud: int = 15) -> str:
        llenos = int(score * longitud)
        return "█" * llenos + "░" * (longitud - llenos)
