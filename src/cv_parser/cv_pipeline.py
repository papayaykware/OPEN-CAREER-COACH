"""Pipeline de procesamiento de currículums para el MVP."""

import re
from typing import List, Optional
from dataclasses import dataclass, field

from src.config import TECH_SKILLS, SOFT_SKILLS
from src.utils.file_loader import load_text_from_file


@dataclass
class CVData:
    raw_text: str = ""
    skills_technical: List[str] = field(default_factory=list)
    skills_soft: List[str] = field(default_factory=list)
    experience_years: Optional[float] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    file_format: str = ""
    pages: int = 0


class CVPipeline:
    """Pipeline completo de procesamiento de CVs."""

    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}")
    LINKEDIN_PATTERN = re.compile(r"linkedin\.com/in/[\w-]+")

    def __init__(self) -> None:
        self.tech_skills_lower = {s.lower() for s in TECH_SKILLS}
        self.soft_skills_lower = {s.lower() for s in SOFT_SKILLS}

    def process(self, file_path: str) -> CVData:
        extraction = load_text_from_file(file_path)
        return self._build_cv_data(
            text=extraction["text"],
            file_format=extraction["format"],
            pages=extraction.get("pages_estimated", 0),
        )

    def process_text(self, text: str) -> CVData:
        """Procesa texto de CV ya extraído/pegado, sin pasar por un archivo en disco.

        Útil para interfaces (Gradio, API, etc.) donde el usuario pega el texto
        directamente en lugar de subir un PDF/DOCX/TXT.
        """
        return self._build_cv_data(text=text, file_format="TEXT", pages=0)

    def _build_cv_data(self, text: str, file_format: str, pages: int) -> CVData:
        cv_data = CVData(
            raw_text=text,
            file_format=file_format,
            pages=pages,
        )

        cv_data.email = self._extract_email(text)
        cv_data.phone = self._extract_phone(text)
        cv_data.linkedin = self._extract_linkedin(text)

        tech, soft = self._extract_skills(text)
        cv_data.skills_technical = tech
        cv_data.skills_soft = soft

        cv_data.experience_years = self._estimate_experience(text)

        return cv_data

    def _extract_email(self, text: str) -> Optional[str]:
        match = self.EMAIL_PATTERN.search(text)
        return match.group() if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        match = self.PHONE_PATTERN.search(text)
        return match.group() if match else None

    def _extract_linkedin(self, text: str) -> Optional[str]:
        match = self.LINKEDIN_PATTERN.search(text)
        return match.group() if match else None

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

    def _estimate_experience(self, text: str) -> Optional[float]:
        text_lower = text.lower()
        patterns = [
            r"(\d+)\+?\s*(?:years?|años?)(?:\s+of)?(?:\s+experience)?",
            r"(?:experiencia(?:\s+de)?\s+)(\d+)\s*(?:años?|years?)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    years = [int(m) for m in matches if m.isdigit()]
                    if years:
                        return float(min(years))
                except Exception:
                    continue

        return None
