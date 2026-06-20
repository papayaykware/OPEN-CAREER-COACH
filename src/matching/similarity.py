"""Motor de matching semántico entre CVs y ofertas de empleo."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class MatchResult:
    global_score: float
    semantic_similarity: float
    skill_match_score: float
    experience_match_score: float
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    extra_skills: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class CVJobMatcher:
    """Motor de matching entre currículums y ofertas de empleo."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def calculate_match(self, cv_data: Dict, job_data: Dict) -> MatchResult:
        semantic_sim = self._calculate_semantic_similarity(
            cv_data.get("raw_text", ""),
            job_data.get("raw_text", ""),
        )

        skill_score, matched, missing, extra = self._calculate_skill_match(
            cv_data.get("skills_technical", []),
            job_data.get("required_skills", []),
        )

        exp_score = self._calculate_experience_match(
            cv_data.get("experience_years"),
            job_data.get("experience_years"),
            job_data.get("experience_range"),
        )

        global_score = 0.40 * semantic_sim + 0.40 * skill_score + 0.20 * exp_score

        recommendations = self._generate_recommendations(missing, cv_data, job_data)

        return MatchResult(
            global_score=round(global_score, 1),
            semantic_similarity=round(semantic_sim, 1),
            skill_match_score=round(skill_score, 1),
            experience_match_score=round(exp_score, 1),
            matched_skills=matched,
            missing_skills=missing,
            extra_skills=extra,
            recommendations=recommendations,
        )

    def _calculate_semantic_similarity(self, cv_text: str, job_text: str) -> float:
        if not cv_text or not job_text:
            return 0.0

        embeddings = self.model.encode([cv_text, job_text])
        cv_emb, job_emb = embeddings[0], embeddings[1]

        num = float(np.dot(cv_emb, job_emb))
        den = float(np.linalg.norm(cv_emb) * np.linalg.norm(job_emb))
        if den == 0:
            return 0.0

        cos_sim = num / den
        return max(0.0, min(1.0, cos_sim)) * 100.0

    def _calculate_skill_match(
        self,
        cv_skills: List[str],
        job_skills: List[str],
    ) -> Tuple[float, List[str], List[str], List[str]]:
        cv_set = {s.lower() for s in cv_skills}
        job_set = {s.lower() for s in job_skills}

        matched = sorted(cv_set & job_set)
        missing = sorted(job_set - cv_set)
        extra = sorted(cv_set - job_set)

        if not job_set:
            score = 100.0 if cv_set else 0.0
        else:
            score = (len(matched) / len(job_set)) * 100.0

        return score, matched, missing, extra

    def _calculate_experience_match(
        self,
        cv_years: Optional[float],
        job_years: Optional[int],
        job_range: Optional[Tuple[int, int]],
    ) -> float:
        if cv_years is None and job_years is None and job_range is None:
            return 50.0

        if cv_years is None:
            return 0.0

        if job_range:
            min_y, max_y = job_range
            if cv_years < min_y:
                diff = min_y - cv_years
                return max(0.0, 100.0 - diff * 20.0)
            if cv_years > max_y:
                return 100.0
            return 100.0

        if job_years is not None:
            if cv_years >= job_years:
                return 100.0
            diff = job_years - cv_years
            return max(0.0, 100.0 - diff * 20.0)

        return 50.0

    def _generate_recommendations(
        self,
        missing_skills: List[str],
        cv_data: Dict,
        job_data: Dict,
    ) -> List[str]:
        recs: List[str] = []

        if missing_skills:
            recs.append(
                "Refuerza o adquiere las siguientes skills clave para este puesto: "
                + ", ".join(missing_skills)
            )

        if cv_data.get("experience_years") is not None and job_data.get("experience_years"):
            if cv_data["experience_years"] < job_data["experience_years"]:
                recs.append(
                    "Considera destacar proyectos o experiencias adicionales que muestren responsabilidad equivalente "
                    "aunque no sumen años formales."
                )

        if not recs:
            recs.append("Tu perfil está bien alineado con la oferta. Ajusta el CV para resaltar los puntos fuertes.")

        return recs
