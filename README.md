# OPEN CAREER COACH - MVP

MVP para análisis de matching entre currículums y ofertas de empleo.

## Estructura

- `src/config.py` — Configuración global.
- `src/utils/file_loader.py` — Carga de archivos CV.
- `src/cv_parser/cv_pipeline.py` — Parsing de CVs.
- `src/job_parser/job_pipeline.py` — Parsing de ofertas.
- `src/matching/similarity.py` — Motor de matching.
- `src/ui/gradio_app.py` — Interfaz mínima en Gradio.

## Uso rápido

```bash
pip install -r requirements.txt
python -m src.ui.gradio_app
```
