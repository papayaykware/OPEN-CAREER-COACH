def parse_cv(texto_cv: str) -> dict:
    """Extrae información básica del CV."""
    return {
        "skills": [s.strip() for s in texto_cv.split(",")],
        "raw": texto_cv
    }
