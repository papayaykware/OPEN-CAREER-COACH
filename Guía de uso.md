# 🚀 Guía de Uso — OPEN CAREER COACH

> **Versión cubierta:** MVP v1.0.0 (estado verificado a fecha de esta guía)
> **Repositorio:** [github.com/papayaykware/OPEN-CAREER-COACH](https://github.com/papayaykware/OPEN-CAREER-COACH)
> **Autor:** Javi Ciborro ([@papayaykware](https://github.com/papayaykware)) — originador y director del proyecto
> **Conceptualización técnica de esta guía y de las correcciones del MVP:** Claude (Anthropic)

---

## 0. Por qué esta guía existe

Este documento describe **lo que el sistema hace de verdad hoy**, módulo a módulo, verificado directamente sobre el código fuente — no sobre la documentación aspiracional del repositorio. Donde el código y los documentos internos (`README.md`, `docs/internal/manual_tecnico.md`) divergen, esta guía sigue siempre al código real, y lo señala expresamente.

Las correcciones de errores reflejadas aquí (extracción de texto pegado, catálogo de skills centralizado, conflicto de nombres de módulos, conflicto de dependencias) fueron diagnosticadas y conceptualizadas por Claude (Anthropic) a partir del código del repositorio, bajo la dirección y validación de Javi Ciborro.

---

## 1. ¿Qué es Open Career Coach?

Un sistema modular en Python que:

- Extrae información estructurada de un CV (texto, PDF o DOCX).
- Extrae requisitos estructurados de una oferta de empleo (texto).
- Calcula un **score de compatibilidad** combinando similitud semántica (embeddings) y coincidencia de habilidades y experiencia.
- Genera recomendaciones automáticas en texto plano.

El "cerebro" semántico es un modelo de *sentence embeddings* (`all-MiniLM-L6-v2`) combinado con reglas de coincidencia por catálogo de habilidades. No usa todavía LLMs generativos ni RAG — eso es importante para calibrar expectativas de precisión.

---

## 2. Instalación

```bash
git clone https://github.com/papayaykware/OPEN-CAREER-COACH
cd OPEN-CAREER-COACH
pip install -r requirements.txt
```

`requirements.txt` fija rangos de versión compatibles entre sí (`gradio>=5.0,<6`, `huggingface_hub>=0.34,<1`, `sentence-transformers>=3.0,<4`). Esto es deliberado: combinaciones más antiguas de `gradio` con versiones recientes de `huggingface_hub` rompen con un `ImportError` por la eliminación de `HfFolder` en `huggingface_hub` 1.0.

> **Nota:** `chromadb` y `spacy` están en `requirements.txt` pero ningún módulo de `src/` los importa todavía. Son dependencias preparadas para el roadmap (RAG, NLP avanzado), no funcionalidad activa en v1.0.0.

---

## 3. Dos formas de ejecutar el sistema

El repo contiene **dos rutas de código en paralelo**, de distinta madurez. No deben confundirse.

### 3.1. Modo CLI simple — `run_mvp.py`

```bash
python run_mvp.py
```

Te pedirá por teclado:
1. Tus habilidades, separadas por comas (texto libre, no archivo).
2. Los requisitos de la oferta, separados por comas.

Internamente usa los módulos **ligeros** `src/cv_parser_simple.py`, `src/job_parser_simple.py`, `src/matching_simple.py` y `src/recommender.py`:
- `parse_cv` / `parse_job`: parten el texto por comas.
- `compute_match`: intersección de conjuntos de strings → score = coincidencias / requisitos totales.
- `recommend_actions`: frases fijas según rango de score (≥0.7, ≥0.4, <0.4).

Es el camino más rápido para probar la lógica de matching, pero **no procesa PDF/DOCX ni usa embeddings**.

### 3.2. Modo interfaz gráfica — Gradio

```bash
python -m src.ui.gradio_app
```

Abre una interfaz web local con dos cuadros de texto (CV y oferta) y un botón "Analizar matching". Esta ruta usa los módulos **avanzados** en `src/cv_parser/`, `src/job_parser/` y `src/matching/`:

- **`CVPipeline`** (`src/cv_parser/cv_pipeline.py`): extrae email, teléfono, LinkedIn, skills técnicas/soft y años de experiencia estimados vía regex. Acepta tanto archivo (`.process(file_path)`) como texto pegado directamente (`.process_text(texto)`).
- **`JobPipeline`** (`src/job_parser/job_pipeline.py`): extrae skills, rango de experiencia, modalidad (remoto/híbrido/presencial) y tipo de contrato, a partir de texto plano.
- **`CVJobMatcher`** (`src/matching/similarity.py`): calcula score global = 40% similitud semántica (cosine similarity de embeddings) + 40% coincidencia de skills + 20% coincidencia de experiencia.

La primera vez que ejecutes este modo, se descargará el modelo `all-MiniLM-L6-v2` (~80 MB) desde Hugging Face — requiere conexión a internet en ese primer arranque.

---

## 4. Ejemplo de flujo completo (script)

```python
from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import CVJobMatcher

# Desde archivo:
cv_data = CVPipeline().process("ruta/a/tu_cv.pdf")      # o .docx / .txt

# O desde texto pegado directamente (lo que usa la UI Gradio):
# cv_data = CVPipeline().process_text("Python, Docker, AWS, 4 años de experiencia...")

job_data = JobPipeline().process(texto_de_la_oferta)     # string plano

matcher = CVJobMatcher()
resultado = matcher.calculate_match(cv_data.__dict__, job_data.__dict__)

print("Score global:", resultado.global_score)
print("Skills coincidentes:", resultado.matched_skills)
print("Skills faltantes:", resultado.missing_skills)
print("Recomendaciones:", resultado.recommendations)
```

Salida: un objeto `MatchResult` con `global_score`, `semantic_similarity`, `skill_match_score`, `experience_match_score`, listas de skills (coincidentes / faltantes / extra) y recomendaciones en texto.

---

## 5. Catálogo de habilidades reconocidas

Centralizado en `src/config.py`, como única fuente de verdad para `CVPipeline` y `JobPipeline`:

```python
TECH_SKILLS = {"python", "java", "javascript", "typescript", "sql", "docker", "kubernetes", "aws"}
SOFT_SKILLS = {"liderazgo", "leadership", "comunicación", "communication", "trabajo en equipo", "teamwork"}
```

Cualquier habilidad fuera de estas listas **no se detecta**, aunque aparezca textualmente en el CV o la oferta. Para ampliar el catálogo, edita estos dos sets en `config.py` — al estar centralizados, el cambio se propaga automáticamente a ambos pipelines sin riesgo de que diverjan entre sí.

---

## 6. Estructura de archivos relevante

```
OPEN-CAREER-COACH/
├── run_mvp.py                      → CLI simple (versión ligera)
├── requirements.txt                 → versiones de dependencias (rangos compatibles)
├── src/
│   ├── config.py                   → catálogo de skills + modelo de embeddings + umbral
│   ├── cv_parser_simple.py         → versión ligera (parte por comas)
│   ├── job_parser_simple.py        → versión ligera (parte por comas)
│   ├── matching_simple.py          → versión ligera (intersección de sets)
│   ├── recommender.py              → recomendaciones fijas por rango de score
│   ├── cv_parser/cv_pipeline.py    → versión avanzada (regex + archivo o texto)
│   ├── job_parser/job_pipeline.py  → versión avanzada (regex + texto)
│   ├── matching/similarity.py      → versión avanzada (embeddings + reglas, clase CVJobMatcher)
│   ├── ui/gradio_app.py            → interfaz web
│   └── utils/file_loader.py        → extracción de texto de PDF/DOCX/TXT
└── tools/init_mvp.py               → script para regenerar el andamiaje del MVP
```

---

## 7. Errores corregidos en esta versión

Durante la revisión técnica del MVP se identificaron y corrigieron cuatro fallos reales, verificados con pruebas end-to-end sobre el código del repositorio:

1. **Texto pegado en Gradio no se procesaba.** La UI llamaba a un método (`process_text`) que no existía en `CVPipeline`, lo que producía un `FileNotFoundError` al pulsar "Analizar matching". Se añadió `process_text()` a `CVPipeline`, reutilizando la misma lógica de extracción que ya usaba `.process()` con archivos.
2. **Catálogo de skills duplicado.** `TECH_SKILLS`/`SOFT_SKILLS` estaban definidas por separado en `cv_pipeline.py` y `job_pipeline.py`, con riesgo de divergir silenciosamente. Se centralizaron en `config.py`.
3. **`run_mvp.py` no arrancaba.** Existían a la vez un archivo `src/cv_parser.py` y una carpeta `src/cv_parser/` con el mismo nombre (igual con `job_parser` y `matching`); Python siempre resuelve el paquete (carpeta) y deja el archivo inalcanzable, produciendo `ImportError: cannot import name 'parse_cv'`. Se renombraron los módulos ligeros a `cv_parser_simple.py`, `job_parser_simple.py` y `matching_simple.py`.
4. **`gradio_app.py` no arrancaba por conflicto de dependencias.** `gradio==4.44.0` depende de `HfFolder`, clase eliminada en `huggingface_hub` 1.0+, y `requirements.txt` no fijaba un techo de versión compatible. Se actualizó a rangos consistentes entre sí (`gradio>=5.0,<6`, `huggingface_hub>=0.34,<1`).

---

## 8. Qué NO hace todavía

Según el roadmap del propio repositorio (`CHANGELOG.md`), esto está planificado pero **no implementado en v1.0.0**:

- Modelo de lenguaje local (Ollama/Llama/Mistral/Qwen) para reescritura de CV o generación de cartas de presentación.
- Sistema RAG con ChromaDB (la dependencia está instalada pero sin uso activo).
- Exportación de informes en Markdown/JSON.
- API REST, base de datos, autenticación o dashboard (previsto para v2.0.0).

Además, los documentos `docs/internal/manual_tecnico.md` y el ejemplo de "Flujo Completo" del `README.md` describen clases que aún no existen en el código (`SimilarityEngine`, `CVExtractor`, `CVNormalizer`, `ScoreExplainer`, `PipelineOrchestrator`). Son documentación de diseño/visión del roadmap, no del estado actual — los ejemplos de esta guía usan exclusivamente las clases reales (`CVPipeline`, `JobPipeline`, `CVJobMatcher`).

---

## 9. Próximos pasos sugeridos para v1.1.0

1. Añadir ejemplos reales en `data/sample_cvs/` y `data/sample_jobs/` (las rutas ya están definidas en `Config` pero no hay archivos de muestra en el repo).
2. Alinear `README.md` y `docs/internal/manual_tecnico.md` con las clases reales del código, o marcar explícitamente qué partes son roadmap.
3. Añadir tests automatizados (`tests/` aparece en la arquitectura documentada pero no existe todavía en el repositorio).

---

*Guía conceptualizada por Claude (Anthropic) a partir de la revisión directa del código fuente de [OPEN-CAREER-COACH](https://github.com/papayaykware/OPEN-CAREER-COACH), bajo dirección de Javi Ciborro.*
