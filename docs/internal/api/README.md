# 🧩 Documentación API Interna  
*(lista para copiar en `docs/internal/api/README.md`)*

## 📘 Índice de la API
- [API del módulo cv_parser](#api-del-módulo-cv_parser)
- [API del módulo job_parser](#api-del-módulo-job_parser)
- [API del módulo matching](#api-del-módulo-matching)
- [API del módulo ui](#api-del-módulo-ui)
- [API del módulo utils](#api-del-módulo-utils)

---

# 🧠 API del módulo `cv_parser`

## Clase: `CVPipeline`
Pipeline principal para procesar CVs.

### Métodos
- **process(path: str) → dict**  
  Procesa un CV desde un archivo PDF, DOCX o TXT.  
  Devuelve una representación estructurada.

- **clean_text(text: str) → str**  
  Normaliza y limpia el texto.

- **extract_sections(text: str) → dict**  
  Identifica secciones como educación, experiencia, habilidades.

---

## Clase: `CVExtractor`
Encargada de la extracción bruta del texto.

### Métodos
- **from_pdf(path: str) → str**  
- **from_docx(path: str) → str**  
- **from_txt(path: str) → str**

---

## Clase: `CVNormalizer`
Estandariza el contenido del CV.

### Métodos
- **normalize_sections(sections: dict) → dict**  
- **normalize_skills(skills: list[str]) → list[str]**

---

# 📄 API del módulo `job_parser`

## Clase: `JobPipeline`
Pipeline principal para procesar ofertas de empleo.

### Métodos
- **process(path: str) → dict**  
  Devuelve una estructura con requisitos, habilidades y descripción.

- **extract_requirements(text: str) → list[str]**  
- **extract_skills(text: str) → list[str]**

---

## Clase: `JobExtractor`
Encargada de la extracción del texto.

### Métodos
- **from_file(path: str) → str**  
- **from_url(url: str) → str**

---

## Clase: `JobNormalizer`
Estandariza la oferta.

### Métodos
- **normalize_requirements(reqs: list[str]) → list[str]**  
- **normalize_skills(skills: list[str]) → list[str]**

---

# 🔍 API del módulo `matching`

## Clase: `SimilarityEngine`
Motor principal de matching semántico.

### Métodos
- **compare(cv: dict, job: dict) → float**  
  Devuelve un score entre 0 y 1.

- **explain(cv: dict, job: dict) → dict**  
  Devuelve una explicación del matching.

- **embed(text: str) → list[float]**  
  Genera embeddings.

---

## Clase: `EmbeddingModel`
Abstracción del modelo de embeddings.

### Métodos
- **load()**  
- **encode(text: str) → list[float]**

---

## Clase: `ScoreExplainer`
Genera explicaciones del score.

### Métodos
- **explain_similarity(cv_vec, job_vec) → dict**  
- **highlight_matches(cv: dict, job: dict) → dict**

---

# 🖥️ API del módulo `ui`

## Clase: `GradioApp`
Interfaz principal.

### Métodos
- **launch()**  
  Inicia la interfaz.

- **predict(cv_file, job_file) → dict**  
  Ejecuta el pipeline completo.

---

## Clase: `PipelineOrchestrator`
Coordina CV → Job → Matching.

### Métodos
- **run(cv_path: str, job_path: str) → dict**  
- **validate_inputs(cv_path, job_path)**

---

# 🧰 API del módulo `utils`

## Funciones principales

- **clean_text(text: str) → str**  
- **normalize_string(s: str) → str**  
- **load_json(path: str) → dict**  
- **save_json(path: str, data: dict)**  
- **log(message: str, level: str = "INFO")**

---

# 🧪 Ejemplo de uso de la API

```python
from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import SimilarityEngine

cv = CVPipeline().process("cv.pdf")
job = JobPipeline().process("job.txt")

engine = SimilarityEngine()
score = engine.compare(cv, job)
explanation = engine.explain(cv, job)

print(score)
print(explanation)
```
