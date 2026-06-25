"""
OPEN-CAREER-COACH · src/matching/explainer.py
Matching Explicable — v1.1.0

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import re


# ─────────────────────────────────────────────
# ESTRUCTURAS DE DATOS
# ─────────────────────────────────────────────

@dataclass
class DimensionScore:
    """Score de similitud para una dimensión semántica concreta."""
    dimension: str
    score: float          # 0.0 – 1.0
    weight: float         # peso en el score final ponderado
    cv_fragments: list[str] = field(default_factory=list)
    offer_fragments: list[str] = field(default_factory=list)


@dataclass
class RequirementMatch:
    """Evaluación de un requisito individual de la oferta contra el CV."""
    requirement: str
    status: str           # "cubierto" | "parcial" | "ausente"
    confidence: float     # 0.0 – 1.0
    cv_evidence: Optional[str] = None


@dataclass
class ExplainedMatchResult:
    """Resultado completo del matching explicable."""
    global_score: float
    dimension_scores: list[DimensionScore]
    gap_analysis: list[RequirementMatch]
    strengths: list[str]
    gaps: list[str]
    narrative: str
    metadata: dict = field(default_factory=dict)


# ─────────────────────────────────────────────
# CONFIGURACIÓN DE DIMENSIONES Y PESOS
# ─────────────────────────────────────────────

DEFAULT_DIMENSIONS = {
    "habilidades_tecnicas": 0.35,
    "experiencia":          0.25,
    "formacion":            0.15,
    "habilidades_blandas":  0.15,
    "idiomas":              0.10,
}

# Patrones de segmentación por dimensión (heurísticos, extensibles)
DIMENSION_PATTERNS = {
    "habilidades_tecnicas": [
        r"\b(python|java|sql|excel|power\s*bi|tableau|r\b|machine\s*learning|"
        r"deep\s*learning|nlp|docker|kubernetes|aws|azure|gcp|api|rest|"
        r"tensorflow|pytorch|scikit)\b"
    ],
    "experiencia": [
        r"\b(\d+\s*años?\s*de\s*experiencia|experiencia\s*en|"
        r"trabajé\s*en|desarrollé|lideré|gestioné|coordiné|"
        r"empresa|compañía|cargo|puesto|rol)\b"
    ],
    "formacion": [
        r"\b(grado|máster|doctorado|licenciatura|diplomatura|"
        r"certificación|bootcamp|curso|formación|universidad|"
        r"escuela|facultad|título)\b"
    ],
    "habilidades_blandas": [
        r"\b(trabajo\s*en\s*equipo|liderazgo|comunicación|"
        r"resolución\s*de\s*problemas|adaptabilidad|proactividad|"
        r"orientación\s*a\s*resultados|autonomía|creatividad)\b"
    ],
    "idiomas": [
        r"\b(español|inglés|francés|alemán|portugués|italiano|"
        r"chino|árabe|b1|b2|c1|c2|nativo|bilingüe|fluido|"
        r"nivel\s*\w+)\b"
    ],
}


# ─────────────────────────────────────────────
# MOTOR PRINCIPAL
# ─────────────────────────────────────────────

class MatchingExplainer:
    """
    Extiende el motor de similitud coseno con explicabilidad estructurada.

    Niveles de análisis:
        1. Descomposición por dimensiones semánticas
        2. Gap analysis por requisito
        3. Score ponderado + narrativa en lenguaje natural

    Uso:
        explainer = MatchingExplainer()
        result = explainer.explain(cv_text, offer_text)
        print(result.narrative)
        print(result.global_score)
    """

    def __init__(
        self,
        dimension_weights: Optional[dict[str, float]] = None,
        similarity_engine=None,
    ):
        self.weights = dimension_weights or DEFAULT_DIMENSIONS
        self._validate_weights()

        # Permite inyectar el SimilarityEngine existente o usa fallback interno
        self.similarity_engine = similarity_engine or self._default_similarity

    def _validate_weights(self):
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Los pesos de dimensión deben sumar 1.0. Suma actual: {total:.3f}"
            )

    # ── Nivel 1: Descomposición dimensional ──────────────────────────────

    def _extract_dimension_fragments(
        self, text: str, dimension: str
    ) -> list[str]:
        """Extrae fragmentos de texto relevantes para una dimensión."""
        patterns = DIMENSION_PATTERNS.get(dimension, [])
        fragments = []
        text_lower = text.lower()
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            fragments.extend(matches)
        return list(set(fragments))

    def _score_dimension(
        self, cv_text: str, offer_text: str, dimension: str
    ) -> DimensionScore:
        cv_fragments = self._extract_dimension_fragments(cv_text, dimension)
        offer_fragments = self._extract_dimension_fragments(offer_text, dimension)

        if not offer_fragments:
            # Si la oferta no menciona esta dimensión, score neutro
            score = 0.5
        elif not cv_fragments:
            score = 0.0
        else:
            # Jaccard sobre conjuntos de términos detectados
            cv_set = set(cv_fragments)
            offer_set = set(offer_fragments)
            intersection = cv_set & offer_set
            union = cv_set | offer_set
            score = len(intersection) / len(union) if union else 0.0

        return DimensionScore(
            dimension=dimension,
            score=round(score, 4),
            weight=self.weights[dimension],
            cv_fragments=cv_fragments,
            offer_fragments=offer_fragments,
        )

    def _compute_dimension_scores(
        self, cv_text: str, offer_text: str
    ) -> list[DimensionScore]:
        return [
            self._score_dimension(cv_text, offer_text, dim)
            for dim in self.weights
        ]

    # ── Nivel 2: Gap analysis ─────────────────────────────────────────────

    def _extract_requirements(self, offer_text: str) -> list[str]:
        """
        Extrae requisitos de la oferta como unidades evaluables.
        Heurístico: oraciones que contienen verbos de requisito o keywords.
        """
        requirement_markers = re.compile(
            r"\b(se\s*requiere|requisito|necesario|imprescindible|"
            r"valorable|deseable|buscamos|el\s*candidato\s*debe|"
            r"experiencia\s*en|conocimientos\s*de|dominio\s*de)\b",
            re.IGNORECASE,
        )
        sentences = re.split(r"[.\n;]", offer_text)
        requirements = [
            s.strip()
            for s in sentences
            if requirement_markers.search(s) and len(s.strip()) > 10
        ]
        return requirements[:20]  # cap para performance

    def _evaluate_requirement(
        self, requirement: str, cv_text: str
    ) -> RequirementMatch:
        """Evalúa si un requisito está cubierto en el CV."""
        # Extrae términos clave del requisito (no stopwords)
        stopwords = {
            "se", "el", "la", "los", "las", "un", "una", "de", "en",
            "que", "con", "y", "o", "a", "es", "son", "para", "por",
            "del", "al", "su", "sus"
        }
        tokens = [
            w.lower()
            for w in re.findall(r"\b\w{3,}\b", requirement)
            if w.lower() not in stopwords
        ]
        if not tokens:
            return RequirementMatch(
                requirement=requirement,
                status="ausente",
                confidence=0.0,
            )

        cv_lower = cv_text.lower()
        matches = [t for t in tokens if t in cv_lower]
        ratio = len(matches) / len(tokens)

        if ratio >= 0.6:
            status = "cubierto"
        elif ratio >= 0.25:
            status = "parcial"
        else:
            status = "ausente"

        evidence = ", ".join(matches) if matches else None

        return RequirementMatch(
            requirement=requirement[:120],
            status=status,
            confidence=round(ratio, 4),
            cv_evidence=evidence,
        )

    def _run_gap_analysis(
        self, cv_text: str, offer_text: str
    ) -> list[RequirementMatch]:
        requirements = self._extract_requirements(offer_text)
        return [
            self._evaluate_requirement(req, cv_text)
            for req in requirements
        ]

    # ── Nivel 3: Score ponderado y narrativa ─────────────────────────────

    def _weighted_score(self, dimension_scores: list[DimensionScore]) -> float:
        total = sum(ds.score * ds.weight for ds in dimension_scores)
        return round(total, 4)

    def _build_strengths_and_gaps(
        self, dimension_scores: list[DimensionScore], gap_analysis: list[RequirementMatch]
    ) -> tuple[list[str], list[str]]:
        strengths = [
            f"Dimensión '{ds.dimension}': score {ds.score:.0%}"
            for ds in dimension_scores
            if ds.score >= 0.5
        ]
        gaps = [
            f"Requisito no cubierto: '{rm.requirement[:80]}'"
            for rm in gap_analysis
            if rm.status == "ausente"
        ]
        return strengths, gaps

    def _generate_narrative(
        self,
        global_score: float,
        strengths: list[str],
        gaps: list[str],
        gap_analysis: list[RequirementMatch],
    ) -> str:
        total_reqs = len(gap_analysis)
        cubiertos = sum(1 for r in gap_analysis if r.status == "cubierto")
        parciales = sum(1 for r in gap_analysis if r.status == "parcial")
        ausentes = sum(1 for r in gap_analysis if r.status == "ausente")

        nivel = (
            "alto" if global_score >= 0.65
            else "moderado" if global_score >= 0.40
            else "bajo"
        )

        narrative = (
            f"El nivel de encaje entre el CV y la oferta es {nivel} "
            f"(score global: {global_score:.0%}).\n\n"
        )

        if total_reqs > 0:
            narrative += (
                f"De {total_reqs} requisitos identificados en la oferta: "
                f"{cubiertos} cubiertos, {parciales} parcialmente cubiertos, "
                f"{ausentes} no presentes en el CV.\n\n"
            )

        if strengths:
            narrative += "Puntos fuertes:\n"
            narrative += "\n".join(f"  · {s}" for s in strengths) + "\n\n"

        if gaps:
            narrative += "Brechas detectadas:\n"
            narrative += "\n".join(f"  · {g}" for g in gaps[:5]) + "\n"

        return narrative.strip()

    # ── Fallback de similitud ─────────────────────────────────────────────

    @staticmethod
    def _default_similarity(text_a: str, text_b: str) -> float:
        """
        Similitud Jaccard de tokens como fallback si no hay SimilarityEngine.
        En producción, sustituir por embeddings del motor existente.
        """
        tokens_a = set(re.findall(r"\b\w{3,}\b", text_a.lower()))
        tokens_b = set(re.findall(r"\b\w{3,}\b", text_b.lower()))
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        return round(len(intersection) / len(union), 4)

    # ── Punto de entrada principal ────────────────────────────────────────

    def explain(
        self,
        cv_text: str,
        offer_text: str,
        profile_type: Optional[str] = None,
    ) -> ExplainedMatchResult:
        """
        Ejecuta el pipeline completo de matching explicable.

        Args:
            cv_text:      Texto extraído del CV (ya procesado por CVPipeline).
            offer_text:   Texto de la oferta (ya procesado por JobPipeline).
            profile_type: Tipo de perfil para ajuste futuro de pesos (opcional).

        Returns:
            ExplainedMatchResult con score, dimensiones, gaps y narrativa.
        """
        dimension_scores = self._compute_dimension_scores(cv_text, offer_text)
        gap_analysis = self._run_gap_analysis(cv_text, offer_text)
        global_score = self._weighted_score(dimension_scores)
        strengths, gaps = self._build_strengths_and_gaps(dimension_scores, gap_analysis)
        narrative = self._generate_narrative(global_score, strengths, gaps, gap_analysis)

        return ExplainedMatchResult(
            global_score=global_score,
            dimension_scores=dimension_scores,
            gap_analysis=gap_analysis,
            strengths=strengths,
            gaps=gaps,
            narrative=narrative,
            metadata={
                "profile_type": profile_type,
                "dimensions_evaluated": list(self.weights.keys()),
            },
        )
