"""
OPEN-CAREER-COACH · run_api.py
Punto de entrada de la API REST — v2.0.0

Uso:
    python run_api.py
    uvicorn src.api.main:app --reload --port 8000

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
