"""Pipeline de procesamiento de ofertas de empleo para el MVP."""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class JobData:
    raw_text: str = ""
    title: str = ""
    company: str = ""
    required_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    experience_years: Optional[int] = None
    experience_range: Optional[Tuple[int, int]] = None
    remote_policy: str = "unknown"
    employment_type: str = "full-time"


class JobPipeline:
    TECH_SKILLS = {
        "python", "java", "javascript", "typescript",
        "sql", "docker", "kubernetes", "aws",
    }

    SOFT_SKILLS = {
        "liderazgo", "leadership", "comunicación", "communication",
        "trabajo en equipo", "teamwork",
    }

    EXPERIENCE_PATTERNS = [
        r"(?:minimum\s+)?(?:(\d+)\+?\s*(?:years?|años?)(?:\s+of)?(?:\s+experience)?)",
        r"(?:(\d+)\s*(?:-|to|a)\s*(\d+)\s*(?:years?|años?))",
    ]

    def __init__(self) -> None:
        self.tech_skills_lower = {s.lower() for s in self.TECH_SKILLS}
        self.soft_skills_lower = {s.lower() for s in self.SOFT_SKILLS}

    def process(self, text: str) -> JobData:
        job = JobData(raw_text=text)
        clean_text = self._preprocess(text)

        tech, soft = self._extract_skills(clean_text)
        job.required_skills = tech
        job.soft_skills = soft

        job.experience_years, job.experience_range = self._extract_experience(clean_text)

        job.remote_policy = self._extract_remote_policy(clean_text)
        job.employment_type = self._extract_employment_type(clean_text)

        return job

    def _preprocess(self, text: str) -> str:
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_skills(self, text: str) -> tuple[list[str], list[str]]:
        text_lower = text.lower()

        tech_found = []
        for skill in self.tech_skills_lower:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                tech_found.append(skill)

        soft_found = []
        for skill in self.soft_skills_lower:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                soft_found.append(skill)

        return sorted(set(tech_found)), sorted(set(soft_found))

    def _extract_experience(self, text: str) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        text_lower = text.lower()

        for pattern in self.EXPERIENCE_PATTERNS:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    try:
                        min_years = int(match[0])
                        max_years = int(match[1])
                        return None, (min_years, max_years)
                    except Exception:
                        continue
                else:
                    try:
                        years = int(match)
                        return years, None
                    except Exception:
                        continue

        return None, None

    def _extract_remote_policy(self, text: str) -> str:
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["100% remote", "fully remote", "remoto 100%", "teletrabajo"]):
            return "remote"
        if any(kw in text_lower for kw in ["hybrid", "híbrido", "mixto"]):
            return "hybrid"
        if any(kw in text_lower for kw in ["on-site", "presencial", "oficina"]):
            return "on-site"

        return "unknown"

    def _extract_employment_type(self, text: str) -> str:
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["full-time", "tiempo completo", "jornada completa"]):
            return "full-time"
        if any(kw in text_lower for kw in ["part-time", "tiempo parcial", "media jornada"]):
            return "part-time"
        if any(kw in text_lower for kw in ["contract", "contrato", "freelance", "autónomo"]):
            return "contract"
        if any(kw in text_lower for kw in ["internship", "prácticas", "becario", "intern"]):
            return "internship"

        return "full-time"
