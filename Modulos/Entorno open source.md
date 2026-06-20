
# MÓDULO 2: Entorno Open Source

> **Duración estimada:** 3-4 horas | **Nivel:** Fundacional

---

## 1. Introducción

Este módulo guía la instalación y configuración del entorno de desarrollo completo para OPEN CAREER COACH. Todas las herramientas son **100% Open Source** y **gratuitas**, eliminando dependencias de APIs pagadas como OpenAI o Azure.

---

## 2. Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Instalar y configurar Python, Git, VS Code y Docker
- ✅ Ejecutar modelos LLM locales con Ollama
- ✅ Crear interfaces web con Gradio y Streamlit
- ✅ Implementar búsqueda vectorial con FAISS y ChromaDB
- ✅ Generar embeddings con Sentence Transformers
- ✅ Construir pipelines con LangChain y LlamaIndex
- ✅ Tomar decisiones informadas sobre stack tecnológico

---

## 3. Fundamentos Teóricos

### 3.1 Por qué Open Source

| Aspecto | Solución Propietaria | Solución Open Source |
|---------|---------------------|---------------------|
| **Coste** | $0.01-0.10/token | $0 (infraestructura propia) |
| **Privacidad** | Datos en servidores externos | Datos locales |
| **Control** | Limitado por API | Total sobre el modelo |
| **Personalización** | Prompt engineering limitado | Fine-tuning completo |
| **Dependencia** | Vendor lock-in | Independencia total |
| **Latencia** | Red + API | Local (<100ms) |

**Trade-off:** Requiere hardware propio (GPU/CPU) y conocimientos técnicos.

### 3.2 Stack Tecnológico Completo

```
┌─────────────────────────────────────────────────────────┐
│                    STACK COMPLETO                       │
├─────────────────────────────────────────────────────────┤
│  Lenguaje:        Python 3.10+                          │
│  Control:         Git                                   │
│  IDE:             VS Code                               │
│  Contenedores:    Docker                                │
│  LLM Local:       Ollama                                │
│  UI Web:          Gradio / Streamlit                    │
│  Vectores:        FAISS / ChromaDB                      │
│  Embeddings:      Sentence Transformers                 │
│  Pipelines:       LangChain / LlamaIndex                │
│  NLP:             spaCy / Transformers (HuggingFace)    │
│  PDF:             PyPDF2 / pdfplumber                   │
│  DOCX:            python-docx                           │
│  Tests:           pytest                                │
│  Linting:         ruff / black                          │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Instalación Paso a Paso

### 4.1 Python 3.10+

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip
python3.10 --version
```

**macOS:**
```bash
brew install python@3.10
python3.10 --version
```

**Windows:**
Descargar desde [python.org](https://www.python.org/downloads/)

### 4.2 Git

```bash
# Linux
sudo apt install git

# macOS
brew install git

# Configurar
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git config --global init.defaultBranch main
```

### 4.3 VS Code

**Extensiones recomendadas:**
- Python (Microsoft)
- Pylance (Microsoft)
- Jupyter (Microsoft)
- Docker (Microsoft)
- GitLens (GitKraken)
- autoDocstring (Nils Werner)
- Python Indent (Kevin Rose)

**Configuración (`settings.json`):**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/*.egg-info": true
    }
}
```

### 4.4 Docker

```bash
# Linux
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Verificar
docker --version
docker-compose --version
```

### 4.5 Ollama (LLMs Locales)

```bash
# Instalar
curl -fsSL https://ollama.com/install.sh | sh

# Verificar
ollama --version

# Descargar modelos
ollama pull llama3.2          # Modelo generalista (4.7GB)
ollama pull mistral           # Alternativa (4.1GB)
ollama pull nomic-embed-text  # Embeddings (274MB)
ollama pull codellama         # Para código (3.8GB)

# Probar
ollama run llama3.2
>>> ¿Qué habilidades buscan las empresas tech en 2026?
```

**Modelos recomendados por tarea:**

| Tarea | Modelo | Tamaño | VRAM Requerida |
|-------|--------|--------|----------------|
| Chat general | llama3.2 | 4.7GB | 6GB |
| Español | mistral | 4.1GB | 6GB |
| Embeddings | nomic-embed-text | 274MB | 1GB |
| Código | codellama | 3.8GB | 5GB |
| Análisis profundo | llama3.2:70b | 40GB | 48GB |

### 4.6 Entorno Virtual Python

```bash
# Crear proyecto
mkdir open-career-coach
cd open-career-coach
git init

# Crear entorno virtual
python3.10 -m venv venv

# Activar
source venv/bin/activate        # Linux/Mac
# venv\\Scripts\\activate       # Windows

# Verificar
which python
# Debe mostrar: .../open-career-coach/venv/bin/python
```

### 4.7 Dependencias Python

Crear `requirements.txt`:

```
# Core
python-dotenv>=1.0.0
pydantic>=2.0.0

# NLP & ML
spacy>=3.7.0
transformers>=4.35.0
sentence-transformers>=2.2.0
torch>=2.1.0

# LLM & RAG
langchain>=0.1.0
langchain-community>=0.0.10
llama-index>=0.9.0

# Vector Stores
faiss-cpu>=1.7.4
chromadb>=0.4.0

# Document Processing
PyPDF2>=3.0.0
python-docx>=1.1.0
pdfplumber>=0.10.0

# UI
gradio>=4.0.0
streamlit>=1.28.0

# Data & Visualization
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.8.0
seaborn>=0.13.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Code Quality
ruff>=0.1.0
black>=23.0.0

# HTTP Client
requests>=2.31.0
httpx>=0.25.0

# Utilities
tqdm>=4.66.0
rich>=13.0.0
```

Instalar:
```bash
pip install -r requirements.txt

# Descargar modelo spaCy español
python -m spacy download es_core_news_md
python -m spacy download en_core_web_md
```

---

## 5. Implementación (Código)

### 5.1 Script de Setup Automático

```python
# scripts/setup.py
"""Script de configuración automática del entorno."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Ejecuta un comando y reporta el resultado."""
    print(f"\\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(e.stderr)
        return False


def check_python_version() -> bool:
    """Verifica que Python sea >= 3.10."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"❌ Python {version.major}.{version.minor} detectado. Se requiere >= 3.10")
    return False


def create_directories() -> None:
    """Crea la estructura de directorios del proyecto."""
    dirs = [
        "data/sample_cvs",
        "data/sample_jobs",
        "data/models",
        "data/vector_stores",
        "src/cv_parser",
        "src/job_parser",
        "src/matching",
        "src/cv_enhancer",
        "src/cover_letter",
        "src/training_recommender",
        "src/rag_system",
        "src/agents",
        "src/evaluation",
        "src/ui",
        "tests",
        "notebooks",
        "scripts",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        # Crear __init__.py en paquetes Python
        if d.startswith("src/") or d == "tests":
            init_file = Path(d) / "__init__.py"
            init_file.touch(exist_ok=True)
    print("✅ Directorios creados")


def check_ollama() -> bool:
    """Verifica si Ollama está instalado y funcionando."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Ollama: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Ollama no encontrado. Instalar: curl -fsSL https://ollama.com/install.sh | sh")
        return False


def pull_models() -> None:
    """Descarga los modelos necesarios."""
    models = ["llama3.2", "nomic-embed-text"]
    for model in models:
        run_command(f"ollama pull {model}", f"Descargando {model}")


def main():
    """Orquesta la configuración completa."""
    print("=" * 60)
    print("🚀 OPEN CAREER COACH - Configuración Automática")
    print("=" * 60)
    
    # Verificaciones
    if not check_python_version():
        sys.exit(1)
    
    # Crear estructura
    create_directories()
    
    # Verificar Ollama
    if check_ollama():
        pull_models()
    else:
        print("\\n⚠️  Ollama no disponible. Instalar manualmente.")
    
    print("\\n" + "=" * 60)
    print("✅ Configuración completada")
    print("=" * 60)
    print("\\nPróximos pasos:")
    print("  1. source venv/bin/activate")
    print("  2. pip install -r requirements.txt")
    print("  3. python -m spacy download es_core_news_md")
    print("  4. python scripts/setup.py")
    print("  5. python -m src.ui.gradio_app")


if __name__ == "__main__":
    main()
```

### 5.2 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    build-essential \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelos spaCy
RUN python -m spacy download es_core_news_md
RUN python -m spacy download en_core_web_md

# Copiar código fuente
COPY . .

# Exponer puertos
EXPOSE 7860 8501 11434

# Script de inicio
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

### 5.3 docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "7860:7860"    # Gradio
      - "8501:8501"    # Streamlit
    volumes:
      - ./data:/app/data
      - ./src:/app/src
      - ollama_models:/root/.ollama
    environment:
      - PYTHONPATH=/app
      - OLLAMA_HOST=0.0.0.0
    depends_on:
      - ollama
    command: python -m src.ui.gradio_app

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  ollama_models:
```

### 5.4 Script de Entrada Docker

```bash
#!/bin/bash
# scripts/entrypoint.sh

echo "🚀 Iniciando OPEN CAREER COACH..."

# Iniciar Ollama en segundo plano
ollama serve &
sleep 5

# Descargar modelos si no existen
ollama pull llama3.2
ollama pull nomic-embed-text

# Ejecutar la aplicación
exec "$@"
```

---

## 6. Explicación Línea a Línea

### setup.py

| Línea | Explicación |
|-------|-------------|
| `subprocess.run(cmd, shell=True, check=True)` | Ejecuta comando del sistema, lanza excepción si falla |
| `Path(d).mkdir(parents=True, exist_ok=True)` | Crea directorios recursivamente, no falla si existen |
| `init_file.touch(exist_ok=True)` | Crea archivo vacío (__init__.py para paquetes Python) |
| `sys.version_info` | Tupla con (major, minor, micro, releaselevel, serial) |

### Dockerfile

| Línea | Explicación |
|-------|-------------|
| `FROM python:3.10-slim` | Imagen base ligera de Python 3.10 |
| `apt-get update && apt-get install -y` | Actualiza e instala dependencias del sistema |
| `--no-cache-dir` | No guarda caché de pip, reduce tamaño de imagen |
| `EXPOSE 7860 8501 11434` | Declara puertos que el contenedor escuchará |
| `ENTRYPOINT ["/entrypoint.sh"]` | Script que se ejecuta al iniciar el contenedor |

### docker-compose.yml

| Línea | Explicación |
|-------|-------------|
| `volumes:` | Monta volúmenes persistentes para datos y modelos |
| `depends_on:` | Asegura que ollama inicie antes que app |
| `deploy.resources.reservations.devices` | Reserva GPU NVIDIA para Ollama |
| `ollama_models:` | Volumen Docker persistente para modelos descargados |

---

## 7. Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| `pip install` muy lento | Sin caché o mirror lento | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| `torch` no instala | Falta CUDA o versión incompatible | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| Ollama no inicia en Docker | Puerto ocupado | `docker-compose down` y `docker system prune` |
| spaCy model no descarga | Proxy o conectividad | Descargar manualmente desde GitHub releases |
| FAISS import error | Falta libomp | `brew install libomp` (Mac) o `apt install libomp-dev` (Linux) |
| Out of memory | Modelo demasiado grande | Usar `llama3.2:3b` en lugar de `llama3.2` |
| Gradio no muestra UI | Puerto no expuesto | Verificar `server_name="0.0.0.0"` en Gradio |

---

## 8. Ejercicios

### 🟢 Nivel Básico

1. **Instalar** todo el stack y verificar con `python scripts/setup.py`.
2. **Probar** Ollama: `ollama run llama3.2` y hacer 5 preguntas en español.
3. **Crear** un entorno virtual nuevo y activarlo/desactivarlo 3 veces.

### 🟡 Nivel Intermedio

4. **Construir** la imagen Docker: `docker-compose up --build`.
5. **Comparar** tiempos de respuesta entre Ollama local y una API online (si tienes acceso).
6. **Configurar** VS Code con debugger para ejecutar paso a paso `setup.py`.

### 🔴 Nivel Avanzado

7. **Optimizar** el Dockerfile usando multi-stage build para reducir tamaño.
8. **Configurar** GPU passthrough en Docker para acelerar Ollama.
9. **Crear** un Makefile con targets: `install`, `test`, `run`, `docker-build`, `docker-run`.

---

## 9. Reto Profesional

**Escenario:** Tu empresa tiene políticas de "no cloud" para datos de RRHH. Debes desplegar OPEN CAREER COACH en un servidor on-premise con:
- CPU: Intel Xeon 16 cores
- RAM: 64GB
- GPU: NVIDIA RTX 4090 (24GB VRAM)
- OS: Ubuntu 22.04 LTS

**Entregable:**
- Documento de instalación paso a paso
- Script de despliegue automatizado
- Configuración de systemd para servicios persistentes
- Plan de backup de modelos y datos
- Estimación de throughput (CVs/hora)

---

## 📚 Recursos Adicionales

- [Ollama GitHub](https://github.com/ollama/ollama)
- [Docker Docs](https://docs.docker.com/)
- [Gradio Docs](https://www.gradio.app/docs)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [LangChain Concepts](https://python.langchain.com/docs/concepts/)

---

**[⬅️ Módulo 1: Arquitectura](01-arquitectura.md) | [➡️ Módulo 3: Procesamiento de CV](03-procesamiento-cv.md)**
'''

