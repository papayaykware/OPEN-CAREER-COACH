# 🚀 OPEN‑CAREER‑COACH  
### Sistema modular de análisis de CVs, ofertas de empleo y matching semántico

![Status](https://img.shields.io/badge/status-MVP%20v1.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Build](https://img.shields.io/badge/build-passing-success)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)

---

# 📑 Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Estructura del Código](#-estructura-del-código)
- [Ejemplo de Flujo Completo](#-ejemplo-de-flujo-completo)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

# 🧠 Descripción General

**Open Career Coach** es un sistema modular diseñado para:

- Analizar CVs en PDF, DOCX o texto.
- Analizar ofertas de empleo.
- Extraer información clave de ambos documentos.
- Calcular el nivel de encaje mediante **similaridad semántica**.
- Mostrar resultados a través de una interfaz ligera con **Gradio**.

El objetivo es ofrecer una base sólida, extensible y profesional para construir herramientas de orientación laboral basadas en IA.

---

# 🏗️ Arquitectura del Proyecto

```
OPEN-CAREER-COACH/
│
├── src/
│   ├── cv_parser/          → Procesamiento de CVs
│   ├── job_parser/         → Procesamiento de ofertas
│   ├── matching/           → Motor de similitud semántica
│   ├── ui/                 → Interfaz Gradio
│   └── utils/              → Utilidades internas
│
├── data/                   → Datos de ejemplo
├── tests/                  → Pruebas unitarias
├── tools/                  → Scripts de soporte
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

---

# ⚙️ Instalación

```bash
git clone https://github.com/papayaykware/OPEN-CAREER-COACH
cd OPEN-CAREER-COACH
pip install -r requirements.txt
```

---

# ▶️ Uso Rápido

Ejecutar la interfaz Gradio:

```bash
python -m src.ui.gradio_app
```

Esto abrirá una interfaz donde podrás:

- Subir un CV  
- Subir una oferta  
- Obtener un **score de matching**  
- Ver explicaciones del análisis  

---

# 🧩 Estructura del Código

### 📄 Procesamiento de CVs  
Módulo: **cv_parser**  
- Limpieza de texto  
- Extracción de secciones  
- Normalización  

### 📄 Procesamiento de ofertas  
Módulo: **job_parser**  
- Extracción de requisitos  
- Identificación de habilidades clave  

### 🔍 Matching semántico  
Módulo: **matching**  
- Embeddings  
- Similaridad coseno  
- Score final  

### 🖥️ Interfaz  
Módulo: **ui**  
- Gradio  
- Flujo completo  

---

# 🔁 Ejemplo de Flujo Completo

```python
from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import SimilarityEngine

cv = CVPipeline().process("cv.pdf")
job = JobPipeline().process("job_offer.txt")

engine = SimilarityEngine()
score = engine.compare(cv, job)

print("Matching:", score)
```

---

# 🗺️ Roadmap

### v1.1.0 (próxima)
- Mejoras en la UI  
- Explicaciones detalladas del matching  
- Exportación de informes  

### v2.0.0
- API REST con FastAPI  
- UI profesional (React / Streamlit)  
- Base de datos  
- Dashboard  

---

# 🤝 Contribuir

Las contribuciones son bienvenidas.  
Puedes abrir un **issue**, enviar un **pull request** o proponer mejoras.

---

# 📄 Licencia

Este proyecto está bajo licencia **MIT**.
