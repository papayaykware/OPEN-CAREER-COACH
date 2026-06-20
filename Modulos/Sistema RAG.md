# 💬 MÓDULO 9: Sistema RAG

> **Duración estimada:** 6-8 horas | **Nivel:** Avanzado

---

## 1. Introducción

Sistema Retrieval-Augmented Generation que permite al usuario hacer preguntas naturales sobre su carrera, comparar con ofertas y recibir respuestas contextualizadas.

---

## 2. Arquitectura RAG

```
Pregunta del Usuario
       │
       ▼
┌─────────────────┐
│  Embedding de   │───▶ nomic-embed-text
│   la pregunta   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Store   │───▶ FAISS / ChromaDB
│  (Búsqueda)     │     Top-k documentos relevantes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Contexto +     │───▶ [Docs recuperados] + [Pregunta]
│   Prompt        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM (Ollama)   │───▶ Genera respuesta con contexto
│  (Generación)   │
└────────┬────────┘
         │
         ▼
   Respuesta + Fuentes
```

---

## 3. Implementación

```python
# src/rag_system/vector_store.py
"""Almacenamiento y búsqueda vectorial."""

import numpy as np
from typing import List, Dict, Optional
import json


class VectorStore:
    """Store de vectores para documentos de carrera."""
    
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.documents: Dict[str, Dict] = {}
        self.vectors: Optional[np.ndarray] = None
        self.index = None
    
    def add_documents(self, documents: List[Dict], embeddings: np.ndarray):
        """Añade documentos con sus embeddings."""
        
        for i, doc in enumerate(documents):
            doc_id = f"doc_{i}"
            self.documents[doc_id] = doc
        
        if self.vectors is None:
            self.vectors = embeddings
        else:
            self.vectors = np.vstack([self.vectors, embeddings])
        
        # Construir índice FAISS
        self._build_index()
    
    def _build_index(self):
        """Construye índice FAISS para búsqueda rápida."""
        try:
            import faiss
            
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner product = cosine for normalized
            self.index.add(self.vectors.astype('float32'))
        except ImportError:
            print("FAISS no disponible, usando búsqueda lineal")
            self.index = None
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Dict]:
        """Busca los k documentos más similares."""
        
        if self.index is not None:
            scores, indices = self.index.search(
                query_embedding.reshape(1, -1).astype('float32'), k
            )
            results = []
            for idx, score in zip(indices[0], scores[0]):
                if idx >= 0 and idx < len(self.documents):
                    doc_id = f"doc_{idx}"
                    doc = self.documents[doc_id].copy()
                    doc["score"] = float(score)
                    results.append(doc)
            return results
        else:
            # Búsqueda lineal fallback
            similarities = np.dot(self.vectors, query_embedding)
            top_indices = np.argsort(similarities)[-k:][::-1]
            
            results = []
            for idx in top_indices:
                doc_id = f"doc_{idx}"
                doc = self.documents[doc_id].copy()
                doc["score"] = float(similarities[idx])
                results.append(doc)
            return results


# src/rag_system/chat_engine.py
"""Motor de chat RAG para carrera profesional."""

import requests
import numpy as np
from typing import List, Dict
from .vector_store import VectorStore
from ..matching.embeddings import EmbeddingGenerator


class CareerChat:
    """Chatbot especializado en carrera profesional."""
    
    SYSTEM_PROMPT = """Eres un asesor de carrera profesional experto. 
Usa el contexto proporcionado para responder preguntas sobre el perfil del usuario.
Sé específico, menciona datos concretos del CV y ofertas.
Si no tienes información suficiente, indícalo claramente."""
    
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.history: List[Dict] = []
    
    def index_cv(self, cv_data: Dict):
        """Indexa el CV del usuario."""
        documents = self._cv_to_documents(cv_data)
        embeddings = self.embedder.generate([d["text"] for d in documents])
        self.vector_store.add_documents(documents, embeddings)
    
    def ask(self, question: str) -> str:
        """Responde una pregunta del usuario."""
        
        # 1. Generar embedding de la pregunta
        question_embedding = self.embedder.generate(question)
        
        # 2. Recuperar contexto relevante
        context_docs = self.vector_store.search(question_embedding, k=3)
        context = "\n\n".join([d["text"] for d in context_docs])
        
        # 3. Construir prompt
        prompt = f"""{self.SYSTEM_PROMPT}

CONTEXTO DEL USUARIO:
{context}

PREGUNTA: {question}

RESPUESTA:"""
        
        # 4. Generar respuesta
        response = self._generate(prompt)
        
        # 5. Guardar en historial
        self.history.append({
            "question": question,
            "response": response,
            "context": context_docs
        })
        
        return response
    
    def _cv_to_documents(self, cv_data: Dict) -> List[Dict]:
        """Convierte CV en documentos para indexar."""
        documents = []
        
        # Documento: información personal
        if cv_data.get("personal_info"):
            info = cv_data["personal_info"]
            documents.append({
                "type": "personal",
                "text": f"Nombre: {info.get('name', '')}. Ubicación: {info.get('location', '')}"
            })
        
        # Documentos: experiencia
        for exp in cv_data.get("experience", []):
            documents.append({
                "type": "experience",
                "text": f"Trabajó como {exp.get('title', '')} en {exp.get('company', '')}. {exp.get('description', '')}"
            })
        
        # Documentos: skills
        skills = cv_data.get("skills", {})
        if skills:
            documents.append({
                "type": "skills",
                "text": f"Skills técnicas: {', '.join(skills.get('technical', []))}. Soft skills: {', '.join(skills.get('soft', []))}"
            })
        
        return documents
    
    def _generate(self, prompt: str) -> str:
        """Genera respuesta con Ollama."""
        response = requests.post(
            self.ollama_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 500}
            }
        )
        return response.json().get("response", "")
```

---

## 4. Ejercicios

### 🟢 Básico
1. Indexar un CV y hacer 5 preguntas de prueba
2. Comparar respuestas con y sin contexto

### 🟡 Intermedio
3. Implementar re-ranking de documentos recuperados
4. Añadir memoria de conversación (multi-turn)

### 🔴 Avanzado
5. Implementar RAG con LangChain/LlamaIndex
6. Sistema de evaluación automática de calidad de respuestas

---

**[⬅️ Módulo 8](08-recomendador-formacion.md) | [➡️ Módulo 10](10-interfaz.md)**
```

