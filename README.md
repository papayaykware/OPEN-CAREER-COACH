
# **"🎯 OPEN CAREER COACH AI Career Coach"**
> 
> Un ecosistema completo de IA para empleabilidad, construido 100% con tecnologías Open Source.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![Gradio](https://img.shields.io/badge/UI-Gradio%20%7C%20Streamlit-orange.svg)](src/ui/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20Local-purple.svg)](https://ollama.com/)

---

## 📋 Índice

- [Visión General](#-visión-general)
- [Arquitectura](#-arquitectura)
- [Módulos](#-módulos)
- [Instalación Rápida](#-instalación-rápida)
- [Uso](#-uso)
- [Roadmaps](#-roadmaps)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🌟 Visión General

**OPEN CAREER COACH** es un asistente inteligente para empleabilidad basado en IA que supera ampliamente al laboratorio original de IBM en:

- 🔬 **Profundidad técnica**: Arquitectura modular con LLMs locales, RAG, embeddings y agentes IA
- 📚 **Pedagogía**: Curso universitario aplicado con 13 módulos progresivos
- 🏗️ **Profesionalismo**: Código de producción, tests, Docker, CI/CD

### Capacidades Principales

| Funcionalidad | Descripción |
|--------------|-------------|
| 📄 **Análisis de CV** | Extrae formación, experiencia, habilidades de PDF/DOCX/TXT |
| 🔍 **Matching Inteligente** | Compara CV con ofertas usando embeddings y similitud semántica |
| ✨ **Mejorador de CV** | Detecta debilidades y reescribe secciones con IA |
| 📝 **Cartas de Presentación** | Genera cartas clásicas, técnicas y ejecutivas personalizadas |
| 🎓 **Recomendador de Formación** | Identifica brechas y genera roadmaps profesionales |
| 💬 **Chat RAG** | Responde preguntas sobre tu trayectoria profesional |
| 📊 **Informes Ejecutivos** | Genera reportes PDF con análisis completos |
| 🤖 **Agentes IA** | Sistema multiagente especializado (ATS, CV, Formación, Entrevistas) |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPEN CAREER COACH                            │
│                     Arquitectura de Alto Nivel                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   Entrada    │     │  Proceso    │     │   Salida    │       │
│  │              │     │             │     │             │       │
│  │  📄 CV      │───▶ │  Pipeline   │───▶│  Matching   │       │
│  │  📋 Oferta  │      │  NLP/LLM    │     │  Score      │      │
│  │  💬 Pregunta │     │  Embeddings │     │  Carta      │      │
│  │              │     │  RAG        │     │  Roadmap    │       │
│  └──────────────┘     └─────────────┘     └─────────────┘       │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              Capa de Almacenamiento                  │       │
│  │  • FAISS (vectores)  • ChromaDB (documentos)         │       │
│  │  • JSON (estructurado)  • SQLite (metadatos)         │       │
│  └──────────────────────────────────────────────────────┘       │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              Capa de Modelos (Ollama Local)          │       │
│  │  • Llama 3.x  • Mistral  • CodeLlama  • Embedding    │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Módulos

| Módulo | Título | Estado |
|--------|--------|--------|
| [M1](docs/01-arquitectura.md) | Arquitectura de un Career Coach basado en IA | ✅ Completo |
| [M2](docs/02-entorno.md) | Entorno Open Source | ✅ Completo |
| [M3](docs/03-procesamiento-cv.md) | Procesamiento de Currículums | ✅ Completo |
| [M4](docs/04-procesamiento-ofertas.md) | Procesamiento de Ofertas de Empleo | ✅ Completo |
| [M5](docs/05-matching.md) | Matching Inteligente | ✅ Completo |
| [M6](docs/06-mejorador-cv.md) | Mejorador Inteligente de CV | ✅ Completo |
| [M7](docs/07-cartas-presentacion.md) | Generador de Cartas de Presentación | ✅ Completo |
| [M8](docs/08-recomendador-formacion.md) | Recomendador de Formación | ✅ Completo |
| [M9](docs/09-sistema-rag.md) | Sistema RAG | ✅ Completo |
| [M10](docs/10-interfaz.md) | Interfaz Profesional | ✅ Completo |
| [M11](docs/11-evaluacion.md) | Evaluación | ✅ Completo |
| [M12](docs/12-despliegue.md) | Despliegue | ✅ Completo |
| [M13](docs/13-agentes-ia.md) | Evolución hacia Agentes IA | ✅ Completo |

---

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.10+
- Git
- Docker (opcional)
- 8GB+ RAM (para modelos locales)

### Opción 1: Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/papayaykware/open-career-coach.git
cd open-career-coach

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Descargar modelos locales (Ollama)
ollama pull llama3.2
ollama pull nomic-embed-text

# 5. Ejecutar aplicación
python -m src.ui.gradio_app
```

### Opción 2: Docker

```bash
# Construir imagen
docker-compose up --build

# Acceder a http://localhost:7860
```

---

## 🎮 Uso

### Análisis de CV

```python
from src.cv_parser.cv_pipeline import CVPipeline

pipeline = CVPipeline()
result = pipeline.process("mi_cv.pdf")
print(result.skills)
print(result.experience)
```

### Matching CV-Oferta

```python
from src.matching.similarity import CVJobMatcher

matcher = CVJobMatcher()
score = matcher.calculate_match(cv_data, job_data)
print(f"Compatibilidad: {score:.1%}")
```

### Chat RAG

```python
from src.rag_system.chat_engine import CareerChat

chat = CareerChat()
response = chat.ask("¿Qué experiencia encaja mejor con esta vacante?")
print(response)
```

---

## 📅 Roadmaps

- [🗓️ Roadmap 30 días](docs/roadmap-30d.md) - Fundamentos + MVP
- [🗓️ Roadmap 90 días](docs/roadmap-90d.md) - Sistema completo + Tests
- [🗓️ Roadmap 180 días](docs/roadmap-180d.md) - Producción + Agentes IA

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <b>Construido con ❤️ y código abierto</b><br>
  <i>Transformando la empleabilidad mediante IA accesible</i>
</p>
"""

with open("/mnt/agents/output/open-career-coach/README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("README.md generado correctamente.")

