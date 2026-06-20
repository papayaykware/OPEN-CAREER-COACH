"""Configuración central del sistema MVP."""

from dataclasses import dataclass


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
