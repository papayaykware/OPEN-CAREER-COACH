# 📌 CHANGELOG — OPEN‑CAREER‑COACH

Este documento recoge los cambios realizados en cada versión del proyecto siguiendo el estándar **Keep a Changelog** y el versionado semántico **SemVer**.

---

## 🟩 [v1.0.0] — 2026-06-20
### 🎉 Primera versión estable (MVP funcional)

#### ✨ Añadido
- Carpeta `src/` con todos los módulos del MVP:
  - `cv_parser` — extracción y normalización de CVs.
  - `job_parser` — análisis de ofertas de empleo.
  - `matching` — cálculo de similitud semántica mediante embeddings.
  - `ui` — interfaz mínima con Gradio.
  - `utils` — utilidades internas.
- Carpeta `data/` con ejemplos y recursos.
- Carpeta `tests/` con estructura inicial de pruebas.
- Script `tools/init_mvp.py` para regenerar el MVP.
- Archivo `requirements.txt` actualizado y funcional.
- `README.md` completo y profesional.

#### 🗑️ Eliminado
- Carpeta antigua `Modulos/` (ya no forma parte del MVP).

#### 🔧 Mejorado
- Estructura del proyecto reorganizada y profesionalizada.
- Claridad del README.
- Preparación para releases futuras.

---

## 🔜 [v1.1.0] — En desarrollo
### Objetivo: Mejoras de UX y estabilidad

#### Previsto
- Integración de modelo local para evitar dependencias externas.
- Mejoras en la interfaz Gradio.
- Explicación detallada del matching.
- Exportación de informes (Markdown / JSON).
- Ejemplos de CV y ofertas listos para usar.

---

## 🔮 [v2.0.0] — Futuro
### Objetivo: Convertir el MVP en un producto completo

#### Previsto
- API REST con FastAPI.
- UI profesional (React / Streamlit).
- Base de datos para almacenar CVs, ofertas y resultados.
- Sistema de autenticación opcional.
- Dashboard de análisis.

---

## 📘 Formato
Este CHANGELOG sigue:
- **Keep a Changelog** — https://keepachangelog.com  
- **Semantic Versioning (SemVer)** — https://semver.org  
