def parse_job(texto_job: str) -> dict:
    """Extrae requisitos básicos de la oferta."""
    return {
        "requirements": [s.strip() for s in texto_job.split(",")],
        "raw": texto_job
    }
