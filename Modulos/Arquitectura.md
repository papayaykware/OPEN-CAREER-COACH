# MÓDULO 1: Arquitectura - versión corregida

modulo1 = '''# 📐 MÓDULO 1: Arquitectura de un Career Coach basado en IA

> **Duración estimada:** 4-6 horas | **Nivel:** Fundacional

---

## 1. Introducción

Este módulo establece los fundamentos conceptuales de OPEN CAREER COACH. Comprenderás cómo se integran las tecnologías de IA para crear un sistema de empleabilidad inteligente, desde la extracción de texto de un PDF hasta la generación de respuestas contextualizadas mediante RAG.

---

## 2. Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Explicar qué es un ATS y cómo funciona
- ✅ Describir el pipeline de NLP aplicado a currículums
- ✅ Diferenciar entre LLM, embeddings y vector databases
- ✅ Comprender el concepto de RAG y fine-tuning
- ✅ Diseñar arquitecturas de sistemas de IA para empleabilidad
- ✅ Leer e interpretar diagramas de arquitectura

---

## 3. Fundamentos Teóricos

### 3.1 ATS (Applicant Tracking System)

Un **ATS** es un software que las empresas utilizan para gestionar procesos de selección. Funciona como un filtro automático que:

1. **Parsea** el CV extrayendo información estructurada
2. **Compara** el CV con la descripción del puesto
3. **Rankea** candidatos según criterios predefinidos
4. **Almacena** datos para búsquedas futuras

**Problema:** Los ATS tradicionales usan palabras clave exactas, penalizando candidatos cualificados que no usan la terminología exacta.

**Solución IA:** Usar embeddings semánticos para entender el significado, no solo las palabras.

### 3.2 NLP (Natural Language Processing)

El NLP es la rama de la IA que permite a las máquinas entender el lenguaje humano. En nuestro contexto:

| Tarea NLP | Aplicación en Career Coach |
|-----------|---------------------------|
| Tokenización | Dividir texto en unidades procesables |
| Named Entity Recognition (NER) | Extraer nombres de empresas, títulos, fechas |
| Part-of-Speech Tagging | Identificar verbos (acciones) vs sustantivos |
| Dependency Parsing | Entender relaciones entre palabras |
| Sentiment Analysis | Evaluar tono del perfil profesional |

### 3.3 LLM (Large Language Model)

Un **LLM** es un modelo de red neuronal entrenado con enormes cantidades de texto. Puede:

- Generar texto coherente
- Responder preguntas
- Resumir documentos
- Traducir entre lenguajes
- Extraer información

**Modelos locales que usaremos:**
- **Llama 3.2** (Meta): Generalista, buen balance calidad/tamaño
- **Mistral** (Mistral AI): Excelente rendimiento en español
- **Nomic Embed Text**: Modelo de embeddings especializado

### 3.4 Embeddings

Un **embedding** es una representación numérica (vector) de texto que captura su significado semántico.

```
"Python developer" → [0.23, -0.87, 0.15, ..., 0.91]  (768 dimensiones)
"Desarrollador Python" → [0.24, -0.86, 0.16, ..., 0.90]  # Muy similar
"Java developer" → [0.25, -0.30, 0.14, ..., 0.45]  # Menos similar
```

**Propiedad clave:** Textos con significado similar tienen vectores cercanos en el espacio vectorial.

### 3.5 Similaridad Semántica

Medimos la cercanía entre vectores usando:

- **Similitud Coseno**: cos(θ) = (A·B) / (||A|| × ||B||)
  - Rango: -1 (opuestos) a +1 (idénticos)
  - Usada en matching CV-oferta

- **Distancia Euclídea**: d = √(Σ(Ai - Bi)²)
  - Mide distancia absoluta entre vectores

- **Producto Punto**: A·B = Σ(Ai × Bi)
  - Considera magnitud y dirección

### 3.6 Vector Databases

Las **vector databases** almacenan y buscan vectores de alta dimensionalidad eficientemente.

| Base de Datos | Tipo | Caso de Uso |
|--------------|------|-------------|
| **FAISS** (Facebook) | Librería C++ con bindings Python | Búsqueda rápida en memoria |
| **ChromaDB** | Nativa Python | Prototipado y desarrollo |
| **Pinecone** | SaaS | Producción escalable |
| **Weaviate** | Open Source | Búsqueda híbrida (vector + BM25) |

**Operaciones principales:**
- `add(vectors, metadata)`: Indexar documentos
- `search(query_vector, k)`: Encontrar los k vecinos más cercanos
- `filter(metadata)`: Filtrar por metadatos antes de búsqueda vectorial

### 3.7 RAG (Retrieval-Augmented Generation)

**RAG** combina recuperación de información con generación de texto:

```
Pregunta del usuario
       │
       ▼
┌─────────────────┐
│  Recuperación   │───▶ Busca documentos relevantes en vector DB
│  (Retrieval)    │     usando embeddings del usuario
└─────────────────┘
       │
       ▼
┌─────────────────┐
│   Contexto      │───▶ Concatena: [Contexto recuperado] + [Pregunta]
│   + Pregunta    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│   Generación    │───▶ LLM genera respuesta basada en contexto
│  (Generation)   │
└─────────────────┘
       │
       ▼
   Respuesta final
```

**Ventajas:**
- Respuestas basadas en datos actualizados
- Reduce alucinaciones del LLM
- Permite citar fuentes
- No requiere reentrenar el modelo

### 3.8 Fine-tuning

El **fine-tuning** adapta un modelo preentrenado a una tarea específica:

```
Modelo Base (Llama 3.2)
       │
       ▼
Datos específicos de empleabilidad
       │
       ▼
Modelo Especializado (Career Coach)
```

**Técnicas modernas:**
- **LoRA** (Low-Rank Adaptation): Entrena solo matrices de bajo rango
- **QLoRA**: LoRA con cuantización de 4 bits
- **Adapter Layers**: Capas pequeñas insertadas entre capas del modelo

### 3.9 Prompt Engineering

El **prompt engineering** es el arte de diseñar instrucciones para obtener mejores respuestas de los LLMs.

**Técnicas clave:**
- **Zero-shot**: Sin ejemplos previos
- **Few-shot**: Con 2-3 ejemplos
- **Chain-of-Thought**: Razonamiento paso a paso
- **ReAct**: Razonamiento + Acción (usado en agentes)

---

## 4. Arquitectura del Sistema

### 4.1 Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OPEN CAREER COACH                                 │
│                         Arquitectura de Alto Nivel                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐                                                          │
│   │   USUARIO    │                                                          │
│   │              │                                                          │
│   │  📄 CV       │                                                          │
│   │  📋 Oferta   │                                                          │
│   │  💬 Pregunta │                                                          │
│   └──────┬───────┘                                                           │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                      CAPA DE PRESENTACIÓN                           │    │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │    │
│   │  │   Gradio    │  │  Streamlit  │  │    API      │                  │    │
│   │  │   (Web UI)  │  │   (Web UI)  │  │   (REST)    │                  │    │
│   │  └─────────────┘  └─────────────┘  └─────────────┘                  │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                    CAPA DE ORQUESTACIÓN                             │    │
│   │  ┌─────────────────────────────────────────────────────────────┐    │    │
│   │  │              Coordinador Multi-Agente                       │    │    │
│   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │    │    │
│   │  │  │ ATS     │ │ CV      │ │ Training│ │Interview│            │    │    │
│   │  │  │ Agent   │ │ Agent   │ │ Agent   │ │ Agent   │            │    │    │
│   │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘            │    │    │
│   │  └─────────────────────────────────────────────────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                    CAPA DE PROCESAMIENTO                            │    │
│   │                                                                     │    │
│   │  ┌─────────────┐     ┌─────────────┐    ┌─────────────┐             │    │
│   │  │   Parser    │     │  Matching   │    │  Enhancer   │             │    │
│   │  │   de CV     │───▶│  Engine     │───▶│  de CV      │             │    │
│   │  │             │     │             │    │             │             │    │
│   │  │ • PDF       │     │ • Embeddings│    │ • Weakness  │             │    │
│   │  │ • DOCX      │     │ • Cosine    │    │   Detector  │             │    │
│   │  │ • TXT       │     │ • Ranking   │    │ • Rewriter  │             │    │
│   │  │ • NER       │     │ • ATS Score │    │ • Keywords  │             │    │
│   │  └─────────────┘     └─────────────┘    └─────────────┘             │    │
│   │                                                                     │    │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │    │
│   │  │   Job       │    │   Cover     │    │  Training   │              │    │
│   │  │   Parser    │    │   Letter    │    │  Recommender│              │    │
│   │  │             │    │   Gen       │    │             │              │    │
│   │  │ • Skills    │    │ • Classic   │    │ • Gap ID    │              │    │
│   │  │ • Tech      │    │ • Technical │    │ • Courses   │              │    │
│   │  │ • Exp Years │    │ • Executive │    │ • Roadmap   │              │    │
│   │  └─────────────┘    └─────────────┘    └─────────────┘              │    │
│   │                                                                     │    │
│   │  ┌─────────────────────────────────────────────────────────────┐    │    │
│   │  │                    Sistema RAG                              │    │    │
│   │  │  • Vector Store (FAISS/ChromaDB)                            │    │    │
│   │  │  • Retriever (Similaridad Semántica)                        │    │    │
│   │  │  • Chat Engine (LangChain/LlamaIndex)                       │    │    │
│   │  └─────────────────────────────────────────────────────────────┘    │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                    CAPA DE MODELOS                                  │    │
│   │                                                                     │    │
│   │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │    │
│   │  │   Ollama        │    │  Sentence       │    │  Transformers   │  │    │
│   │  │   (LLMs)        │    │  Transformers   │    │  (NLP Tasks)    │  │    │
│   │  │                 │    │  (Embeddings)   │    │                 │  │    │
│   │  │ • Llama 3.2     │    │ • all-MiniLM    │    │ • NER           │  │    │
│   │  │ • Mistral       │    │ • nomic-embed   │    │ • Classification│  │    │
│   │  │ • CodeLlama     │    │ • paraphrase    │    │ • Summarization │  │    │
│   │  └─────────────────┘    └─────────────────┘    └─────────────────┘  │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                    CAPA DE ALMACENAMIENTO                           │    │
│   │                                                                     │    │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐   │    │
│   │  │   FAISS     │  │  ChromaDB   │  │   SQLite    │  │   JSON    │   │    │
│   │  │  (Vectors)  │  │ (Documents) │  │ (Metadata)  │  │(Config)   │   │    │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘   │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Flujo de Datos

```
Usuario sube CV (PDF)
       │
       ▼
┌─────────────┐
│  Extractor  │───▶ PyPDF2 / python-docx / textract
│  de Texto   │
└──────┬──────┘
       │ Texto plano
       ▼
┌─────────────┐
│  Pipeline   │───▶ spaCy NER + Transformers
│  NLP        │     Extrae: skills, experiencia, formación
└──────┬──────┘
       │ Datos estructurados (JSON)
       ▼
┌─────────────┐
│  Generador  │───▶ Sentence Transformers
│  Embeddings │     Vector de 384/768 dimensiones
└──────┬──────┘
       │ Vector
       ▼
┌─────────────┐
│  Vector DB  │───▶ FAISS / ChromaDB
│  (Index)    │     Almacena + permite búsqueda
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Matching   │───▶ Similitud coseno con oferta
│  Engine     │     Calcula score de compatibilidad
└──────┬──────┘
       │ Score + Análisis
       ▼
┌─────────────┐
│  LLM        │───▶ Ollama (Llama 3.2)
│  (Ollama)   │     Genera recomendaciones
└──────┬──────┘
       │ Respuesta
       ▼
┌─────────────┐
│   UI        │───▶ Gradio / Streamlit
│  (Output)   │     Muestra resultados al usuario
└─────────────┘
```

---

## 5. Implementación (Código)

### 5.1 Estructura del Proyecto

```python
# src/config.py
"""Configuración central del sistema."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuración global de OPEN CAREER COACH."""
    
    # Modelos
    LLM_MODEL: str = "llama3.2"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    
    # Vector DB
    VECTOR_STORE_TYPE: str = "faiss"
    VECTOR_DIMENSION: int = 768
    
    # Matching
    SIMILARITY_THRESHOLD: float = 0.65
    TOP_K_RESULTS: int = 5
    
    # RAG
    RAG_CHUNK_SIZE: int = 512
    RAG_CHUNK_OVERLAP: int = 50
    RAG_TOP_K: int = 3
    
    # Paths
    DATA_DIR: str = "./data"
    MODELS_DIR: str = "./data/models"
    VECTOR_STORE_DIR: str = "./data/vector_stores"


# Instancia global
config = Config()
```

### 5.2 Clase Base del Sistema

```python
# src/utils.py
"""Utilidades comunes del sistema."""

import json
import hashlib
from typing import Any, Dict, List
from datetime import datetime


class CareerCoachError(Exception):
    """Excepción base del sistema."""
    pass


def generate_id(text: str) -> str:
    """Genera un ID único basado en el contenido."""
    return hashlib.md5(text.encode()).hexdigest()[:12]


def timestamp() -> str:
    """Devuelve timestamp actual en formato ISO."""
    return datetime.now().isoformat()


def save_json(data: Dict[str, Any], path: str) -> None:
    """Guarda datos en formato JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> Dict[str, Any]:
    """Carga datos desde JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class StructuredData:
    """Clase base para datos estructurados del sistema."""
    
    def __init__(self, raw_text: str = ""):
        self.id = generate_id(raw_text)
        self.raw_text = raw_text
        self.created_at = timestamp()
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }
```

---

## 6. Explicación Línea a Línea

### config.py

| Línea | Explicación |
|-------|-------------|
| `@dataclass` | Decorador que genera automáticamente __init__, __repr__, etc. |
| `LLM_MODEL: str = "llama3.2"` | Modelo por defecto, ejecutado localmente via Ollama |
| `VECTOR_DIMENSION: int = 768` | Dimensión de los vectores de embedding |
| `SIMILARITY_THRESHOLD: float = 0.65` | Umbral mínimo para considerar un match válido |

### utils.py

| Línea | Explicación |
|-------|-------------|
| `hashlib.md5(text.encode()).hexdigest()[:12]` | Genera hash MD5 y trunca a 12 caracteres para IDs legibles |
| `datetime.now().isoformat()` | Formato estándar ISO 8601 para timestamps |
| `json.dump(data, f, ensure_ascii=False)` | Permite caracteres Unicode (tildes, ñ) |

---

## 7. Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| "Ollama no encontrado" | Ollama no instalado | `curl -fsSL https://ollama.com/install.sh | sh` |
| "Out of memory" | RAM insuficiente | Usar modelos cuantizados o aumentar swap |
| Embeddings con NaN | Texto vacío | Validar entrada antes de generar embeddings |
| FAISS dimension error | Dimensiones inconsistentes | Asegurar misma dimensión en todos los vectores |
| Matching irrelevante | Umbral bajo | Ajustar SIMILARITY_THRESHOLD a 0.7-0.8 |

---

## 8. Ejercicios

### 🟢 Nivel Básico

1. **Instalar Ollama** y ejecutar `ollama run llama3.2`. Haz 3 preguntas sobre empleabilidad.
2. **Dibujar** el diagrama de arquitectura en papel y explicar cada capa.
3. **Investigar**: ¿Qué es un ATS? Nombra 3 ATS populares.

### 🟡 Nivel Intermedio

4. **Implementar** una función que calcule similitud coseno entre dos vectores aleatorios.
5. **Comparar** FAISS vs ChromaDB: crear tabla con ventajas/desventajas.
6. **Explicar**: ¿por qué RAG es mejor que fine-tuning para datos cambiantes?

### 🔴 Nivel Avanzado

7. **Diseñar** arquitectura alternativa usando microservicios.
8. **Calcular** complejidad temporal de búsqueda en FAISS (IVF) vs exhaustiva.
9. **Investigar** técnicas de cuantización de embeddings.

---

## 9. Reto Profesional

**Escenario:** Eres arquitecto de IA de una startup de RRHH. Diseña un sistema que:
- Procese 10,000 CVs diarios
- Realice matching en <100ms
- Soporte 5 idiomas
- Cumpla GDPR

**Entregable:** Documento de arquitectura con diagrama, stack justificado, estimación de costes y plan de escalabilidad.

---

## 📚 Recursos Adicionales

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [LangChain Docs](https://python.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)

---

**[⬅️ Volver al README](../README.md) | [➡️ Módulo 2: Entorno Open Source](02-entorno.md)**
'''

