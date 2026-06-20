"""Configuración central del sistema MVP."""

from dataclasses import dataclass


# Catálogo centralizado de habilidades reconocidas.
# Única fuente de verdad: tanto CVPipeline como JobPipeline importan estos
# sets en lugar de mantener copias propias, para evitar que ambas listas
# diverjan silenciosamente y rompan el matching.
TECH_SKILLS = {
    "python", "java", "javascript", "typescript",
    "sql", "docker", "kubernetes", "aws",
}

SOFT_SKILLS = {
    "liderazgo", "leadership", "comunicación", "communication",
    "trabajo en equipo", "teamwork",
}


@dataclass
class Config:
    """Configuración global."""

    # Modelos
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Matching
    SIMILARITY_THRESHOLD: float = 0.50

    # Paths
    DATA_DIR: str = "./data"
    SAMPLE_CVS_DIR: str = "./data/sample_cvs"
    SAMPLE_JOBS_DIR: str = "./data/sample_jobs"


config = Config()
