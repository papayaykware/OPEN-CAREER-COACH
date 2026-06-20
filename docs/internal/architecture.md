# 🧩 Documentación interna del proyecto  
*(lista para copiar en `docs/internal/architecture.md`)*

## 🧠 1. Visión general del sistema

El sistema **Open Career Coach** implementa un pipeline modular para:

- Procesar CVs  
- Procesar ofertas  
- Generar representaciones semánticas  
- Calcular similitud  
- Exponer resultados vía interfaz  

El diseño sigue principios de:

- **Separación de responsabilidades**  
- **Modularidad estricta**  
- **Extensibilidad por capas**  
- **Trazabilidad del flujo de datos**  

---

## 🏗️ 2. Arquitectura interna

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

## 📄 3. Módulos internos

### **cv_parser**  
Responsable de:

- Limpieza de texto  
- Extracción de secciones  
- Normalización  
- Representación estructurada del CV  

Clases clave:

- `CVPipeline`  
- `CVExtractor`  
- `CVNormalizer`  

---

### **job_parser**  
Responsable de:

- Extracción de requisitos  
- Identificación de habilidades  
- Representación estructurada de la oferta  

Clases clave:

- `JobPipeline`  
- `JobExtractor`  
- `JobNormalizer`  

---

### **matching**  
Responsable de:

- Generación de embeddings  
- Cálculo de similitud coseno  
- Score final de matching  
- Explicabilidad básica  

Clases clave:

- `SimilarityEngine`  
- `EmbeddingModel`  
- `ScoreExplainer`  

---

### **ui**  
Responsable de:

- Interfaz Gradio  
- Orquestación del pipeline  
- Validación de inputs  

Clases clave:

- `GradioApp`  
- `PipelineOrchestrator`  

---

### **utils**  
Responsable de:

- Logging  
- Normalización  
- Funciones auxiliares  

---

## 🔁 4. Flujo interno de datos

```
CV (PDF/DOCX/TXT)
      ↓
CVPipeline
      ↓
Representación estructurada del CV
      ↓
Embeddings
      ↓
SimilarityEngine
      ↓
Score final + explicación
```

Lo mismo ocurre para la oferta.

---

## 🧬 5. Convenciones internas

- Estilo: PEP8  
- Nombres de clases: PascalCase  
- Nombres de funciones: snake_case  
- Documentación: docstrings tipo Google  
- Tests: un archivo por módulo  
- Logging: nivel INFO por defecto  

---

## 🔌 6. Puntos de extensión

### **Modelos de embeddings**
Puedes sustituir el modelo actual por:

- Modelos locales  
- Modelos open‑source  
- Modelos propietarios  

### **Nuevos parsers**
Puedes añadir:

- Parser de portafolios  
- Parser de GitHub  
- Parser de LinkedIn  

### **Nuevas interfaces**
Puedes extender:

- API REST (FastAPI)  
- UI web (React / Streamlit)  
- CLI  

---

## 🧪 7. Testing interno

Los tests siguen la estructura:

```
tests/
  test_cv_parser.py
  test_job_parser.py
  test_matching.py
```

Cada test valida:

- Integridad del pipeline  
- Consistencia de outputs  
- Robustez ante inputs ruidosos  
