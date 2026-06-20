# 📘 Manual Técnico — OPEN‑CAREER‑COACH  
*(versión completa para desarrolladores)*

## 🧭 1. Propósito del sistema

El sistema **Open Career Coach** implementa un pipeline modular para:

- Procesar CVs  
- Procesar ofertas de empleo  
- Generar representaciones semánticas  
- Calcular similitud  
- Producir explicaciones del matching  
- Exponer resultados mediante una interfaz ligera  

El diseño sigue principios de:

- **Modularidad estricta**  
- **Separación de responsabilidades**  
- **Extensibilidad por capas**  
- **Trazabilidad del flujo de datos**  
- **Bajo acoplamiento, alta cohesión**  

---

# 🧩 2. Arquitectura general del sistema

```
src/
│
├── cv_parser/        → Procesamiento de CVs
├── job_parser/       → Procesamiento de ofertas
├── matching/         → Motor de similitud
├── ui/               → Interfaz Gradio
└── utils/            → Utilidades internas
```

Cada módulo es autónomo y expone una API interna clara.

---

# 🔁 3. Flujo técnico de extremo a extremo

```
CV (PDF/DOCX/TXT)           Oferta (TXT/URL)
        ↓                           ↓
   CVPipeline                  JobPipeline
        ↓                           ↓
 Representación CV         Representación Oferta
        ↓                           ↓
            → Embeddings → SimilarityEngine →
                     Score + Explicación
```

---

# 🧠 4. Diseño interno por módulos

## 📄 Módulo **cv_parser**

### Objetivo
Transformar un CV en una representación estructurada y normalizada.

### Componentes
- `CVPipeline`  
- `CVExtractor`  
- `CVNormalizer`  

### Flujo interno
1. Extracción del texto bruto  
2. Limpieza y normalización  
3. Identificación de secciones  
4. Estandarización de habilidades y experiencia  

### Decisiones técnicas
- Separación extractor/normalizador para permitir nuevos formatos  
- Normalización basada en heurísticas + reglas  

---

## 📄 Módulo **job_parser**

### Objetivo
Convertir una oferta en una estructura comparable con el CV.

### Componentes
- `JobPipeline`  
- `JobExtractor`  
- `JobNormalizer`  

### Flujo interno
1. Extracción del texto  
2. Identificación de requisitos  
3. Extracción de habilidades  
4. Normalización  

### Decisiones técnicas
- Extracción desacoplada para permitir entrada desde URL  
- Normalización compatible con el CV para matching semántico  

---

## 🔍 Módulo **matching**

### Objetivo
Calcular la similitud semántica entre CV y oferta.

### Componentes
- `SimilarityEngine`  
- `EmbeddingModel`  
- `ScoreExplainer`  

### Flujo interno
1. Generación de embeddings  
2. Cálculo de similitud coseno  
3. Agregación ponderada  
4. Explicación del score  

### Decisiones técnicas
- Modelo de embeddings desacoplado → permite modelos locales  
- Explicabilidad basada en diferencias vectoriales  

---

## 🖥️ Módulo **ui**

### Objetivo
Exponer el pipeline mediante una interfaz simple.

### Componentes
- `GradioApp`  
- `PipelineOrchestrator`  

### Flujo interno
1. Validación de inputs  
2. Ejecución del pipeline  
3. Presentación del score y explicación  

### Decisiones técnicas
- UI mínima para facilitar pruebas  
- Orquestador independiente para futuras APIs  

---

## 🧰 Módulo **utils**

Incluye:

- Normalización de texto  
- Logging  
- Carga/guardado de JSON  
- Funciones auxiliares  

---

# 🧬 5. Modelo de datos interno

## Representación del CV

```json
{
  "education": [...],
  "experience": [...],
  "skills": [...],
  "summary": "..."
}
```

## Representación de la oferta

```json
{
  "requirements": [...],
  "skills": [...],
  "description": "..."
}
```

## Representación del matching

```json
{
  "score": 0.87,
  "explanation": {
    "skills_overlap": [...],
    "missing_skills": [...],
    "strengths": [...]
  }
}
```

---

# 🧪 6. Testing técnico

Los tests validan:

- Integridad del pipeline  
- Robustez ante inputs ruidosos  
- Consistencia de embeddings  
- Estabilidad del score  

Estructura:

```
tests/
  test_cv_parser.py
  test_job_parser.py
  test_matching.py
```

---

# 🔌 7. Puntos de extensión

## Modelos de embeddings
Puedes sustituir el modelo actual por:

- Modelos locales  
- Modelos open‑source  
- Modelos propietarios  

## Parsers adicionales
Puedes añadir:

- Parser de LinkedIn  
- Parser de GitHub  
- Parser de portafolios  

## Interfaces adicionales
Puedes extender:

- API REST (FastAPI)  
- UI web (React / Streamlit)  
- CLI  

---

# 🧱 8. Convenciones internas

- Estilo: PEP8  
- Docstrings: formato Google  
- Logging: nivel INFO  
- Tests: pytest  
- Arquitectura: modular, desacoplada  

---

# 🧩 9. Ejemplo técnico completo

```python
from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import SimilarityEngine

cv = CVPipeline().process("cv.pdf")
job = JobPipeline().process("job.txt")

engine = SimilarityEngine()
result = {
    "score": engine.compare(cv, job),
    "explanation": engine.explain(cv, job)
}

print(result)
```
- **Manual de despliegue**  

Dime cuál seguimos, Javier.
