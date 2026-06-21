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
├── run_mvp.py               → CLI simple (entrada rápida sin embeddings)
├── src/
│   ├── config.py             → catálogo de skills + configuración de modelo
│   ├── cv_parser_simple.py   → versión ligera de extracción de CV
│   ├── job_parser_simple.py  → versión ligera de extracción de oferta
│   ├── matching_simple.py    → versión ligera de matching (por palabra clave)
│   ├── recommender.py        → recomendaciones según score
│   ├── cv_parser/            → procesamiento avanzado de CVs (regex + embeddings)
│   ├── job_parser/            → procesamiento avanzado de ofertas
│   ├── matching/              → motor de similitud semántica (CVJobMatcher)
│   ├── ui/                    → interfaz Gradio
│   └── utils/                 → utilidades internas (carga de PDF/DOCX/TXT)
│
├── tools/                   → scripts de soporte (regeneración del andamiaje)
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

> `data/` (CVs y ofertas de ejemplo) y `tests/` (pruebas automatizadas) están previstos en el roadmap pero aún no forman parte del repositorio.

---

# ⚙️ Instalación

```bash
git clone https://github.com/papayaykware/OPEN-CAREER-COACH
cd OPEN-CAREER-COACH
pip install -r requirements.txt
```

---

# ▶️ Uso Rápido

### Opción A — CLI simple (sin instalar modelo de embeddings)

```bash
python run_mvp.py
```

Te pedirá tus habilidades y los requisitos de la oferta por teclado (separados por comas) y devolverá un score básico de coincidencia.

### Opción B — Interfaz Gradio (matching semántico completo)

```bash
python -m src.ui.gradio_app
```

Abre una interfaz web local con dos cuadros de texto donde puedes **pegar** el contenido de tu CV y de la oferta de empleo. Al pulsar "Analizar matching" obtendrás:

- Score global de compatibilidad
- Similitud semántica, match de skills y match de experiencia por separado
- Skills coincidentes y faltantes
- Recomendaciones en texto

La primera ejecución descarga el modelo de embeddings (~80 MB) desde Hugging Face; requiere conexión a internet ese primer arranque.

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
from src.matching.similarity import CVJobMatcher

cv_data = CVPipeline().process("cv.pdf")          # también: .process_text("texto pegado")
job_data = JobPipeline().process("texto de la oferta")

matcher = CVJobMatcher()
resultado = matcher.calculate_match(cv_data.__dict__, job_data.__dict__)

print("Score global:", resultado.global_score)
print("Skills coincidentes:", resultado.matched_skills)
print("Skills faltantes:", resultado.missing_skills)
print("Recomendaciones:", resultado.recommendations)
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
