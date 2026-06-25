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

## 🟦 [v1.0.1] — 2026-06-21
### 🐛 Corrección de errores detectados tras el lanzamiento del MVP

#### 🔧 Corregido
- **UI Gradio no procesaba texto pegado.** `gradio_app.py` llamaba a un método inexistente en `CVPipeline`, lo que producía `FileNotFoundError` al analizar un CV pegado directamente en el cuadro de texto. Se añadió `CVPipeline.process_text()`, reutilizando la lógica de extracción ya existente en `.process()`.
- **`run_mvp.py` no arrancaba.** Existían a la vez un módulo `src/cv_parser.py` y un paquete `src/cv_parser/` con el mismo nombre (igual con `job_parser` y `matching`); Python resolvía siempre el paquete, dejando el módulo inalcanzable y produciendo `ImportError: cannot import name 'parse_cv'`. Los módulos ligeros se renombraron a `cv_parser_simple.py`, `job_parser_simple.py` y `matching_simple.py`.
- **`gradio_app.py` no arrancaba por conflicto de dependencias.** `gradio==4.44.0` depende de `HfFolder`, eliminada en `huggingface_hub` 1.0+, y `requirements.txt` no fijaba un techo de versión compatible. Se actualizaron los rangos a `gradio>=5.0,<6` y `huggingface_hub>=0.34,<1`.
- **Catálogo de skills duplicado.** `TECH_SKILLS`/`SOFT_SKILLS` estaban definidas por separado en `cv_pipeline.py` y `job_pipeline.py`, con riesgo de divergir silenciosamente. Se centralizaron en `src/config.py` como única fuente de verdad.

#### 📝 Documentación
- Corregido el ejemplo de "Flujo Completo" del `README.md`, que referenciaba una clase `SimilarityEngine` inexistente; ahora usa `CVJobMatcher.calculate_match()`, la API real del módulo `matching`.
- Aclarada la sección "Uso Rápido" del `README.md` para distinguir el modo CLI (`run_mvp.py`) del modo interfaz (`gradio_app.py`), y corregido que la UI funciona con texto pegado, no con subida de archivo.

---

## 🔜 [v1.1.0] — En desarrollo

### Objetivo: Matching explicable + tests + exportación de informes

#### ✨ Añadido

- **`src/matching/explainer.py`** — Módulo `MatchingExplainer`: motor de matching
  explicable en tres niveles:
  * Nivel 1: descomposición por dimensiones semánticas (`habilidades_tecnicas`,
    `experiencia`, `formacion`, `habilidades_blandas`, `idiomas`) con scoring
    Jaccard por dimensión e inyección opcional del `SimilarityEngine` existente.
  * Nivel 2: gap analysis estructurado por requisito (`cubierto` / `parcial` /
    `ausente`) con extracción heurística de requisitos en español.
  * Nivel 3: score global ponderado configurable + narrativa en lenguaje natural.
  * Dataclasses `DimensionScore`, `RequirementMatch`, `ExplainedMatchResult`
    como contrato de salida tipado.
  * Compatible con el pipeline actual sin romper la API existente.

- **`tests/test_explainer.py`** — Suite de tests unitarios completa (pytest):
  * 7 clases de test con cobertura de inicialización, extracción dimensional,
    gap analysis, score ponderado, narrativa, integración end-to-end y
    similitud fallback.
  * Fixtures `CV_ALTO_ENCAJE`, `CV_BAJO_ENCAJE` y `OFERTA_DATA_SCIENCE`
    como casos de prueba representativos.
  * Tests de casos límite: textos vacíos, pesos inválidos, CV idéntico a oferta.

#### 🔜 Pendiente en esta versión

- Integración del `MatchingExplainer` en la interfaz Gradio.
- Exportación de informes (PDF / Markdown / JSON).
- Ejemplos de CV y ofertas listos para usar en `data/`.

#### 🏗️ Autoría

- Autor conceptual: Claude (Anthropic)
- Director del proyecto: Javi Ciborro (@papayaykware)

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
