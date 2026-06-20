# ✨ MÓDULO 6: Mejorador Inteligente de CV

> **Duración estimada:** 5-7 horas | **Nivel:** Intermedio

---

## 1. Introducción

Este módulo construye un sistema que analiza currículums, detecta debilidades y los reescribe usando modelos de lenguaje locales.

---

## 2. Objetivos de Aprendizaje

- ✅ Detectar debilidades estructurales en CVs
- ✅ Identificar redundancias y falta de palabras clave
- ✅ Reescribir perfiles profesionales con IA
- ✅ Optimizar experiencia y competencias
- ✅ Evaluar mejoras cuantitativamente

---

## 3. Fundamentos Teóricos

### 3.1 Tipos de Debilidades en CVs

| Debilidad | Descripción | Detección |
|-----------|-------------|-----------|
| **Falta de métricas** | "Aumenté ventas" vs "Aumenté ventas un 150%" | Regex numérico + LLM |
| **Lenguaje pasivo** | "Fui responsable de" vs "Lideré" | POS tagging + verbos |
| **Exceso de texto** | Más de 2 páginas | Contador de tokens |
| **Palabras vacías** | "Proactivo", "Dinámico" sin evidencia | Diccionario + contexto |
| **Falta de keywords** | No contiene términos del sector | Matching con ofertas |
| **Estructura inconsistente** | Fechas desordenadas, formatos mixtos | Parsing de fechas |
| **Secciones incompletas** | Sin formación, sin skills | Validación de campos |

### 3.2 Estrategias de Mejora

```
CV Original
     │
     ▼
┌─────────────┐
│  Análisis   │───▶ Detectar debilidades
│             │
│ • Métricas  │
│ • Verbos    │
│ • Keywords  │
│ • Longitud  │
│ • Estructura│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Rewriting  │───▶ LLM local con prompts especializados
│             │
│ • Perfil    │
│ • Experienc.│
│ • Skills    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Evaluación │───▶ Comparar antes/después
│             │
│ • Score     │
│ • Diff      │
│ • Feedback  │
└─────────────┘
```

---

## 4. Implementación

```python
# src/cv_enhancer/weakness_detector.py
"""Detección de debilidades en currículums."""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Weakness:
    type: str
    severity: str  # low, medium, high
    description: str
    location: str
    suggestion: str


class WeaknessDetector:
    """Detecta debilidades en un CV estructurado."""
    
    # Palabras vacías comunes
    BUZZWORDS = {
        "proactivo", "dinámico", "motivado", "apasionado",
        "proactive", "dynamic", "motivated", "passionate",
        "trabajador", "comprometido", "responsable",
        "hardworking", "committed", "responsible",
    }
    
    # Verbos pasivos
    PASSIVE_VERBS = {
        "fui", "era", "estuve", "me encargué",
        "was", "were", "been", "responsible for",
    }
    
    # Verbos de acción fuertes
    STRONG_VERBS = {
        "lideré", "desarrollé", "implementé", "optimicé",
        "aumenté", "reduje", "creé", "diseñé",
        "led", "developed", "implemented", "optimized",
        "increased", "reduced", "created", "designed",
    }
    
    def detect(self, cv_data: Dict) -> List[Weakness]:
        """Detecta todas las debilidades del CV."""
        weaknesses = []
        
        # 1. Falta de métricas
        weaknesses.extend(self._check_metrics(cv_data))
        
        # 2. Lenguaje pasivo
        weaknesses.extend(self._check_passive_language(cv_data))
        
        # 3. Palabras vacías
        weaknesses.extend(self._check_buzzwords(cv_data))
        
        # 4. Falta de keywords
        weaknesses.extend(self._check_keywords(cv_data))
        
        # 5. Longitud
        weaknesses.extend(self._check_length(cv_data))
        
        # 6. Estructura
        weaknesses.extend(self._check_structure(cv_data))
        
        return weaknesses
    
    def _check_metrics(self, cv_data: Dict) -> List[Weakness]:
        """Verifica presencia de métricas cuantificables."""
        weaknesses = []
        
        for i, exp in enumerate(cv_data.get("experience", [])):
            desc = exp.get("description", "")
            
            # Buscar números seguidos de %
            has_percentage = bool(re.search(r'\d+%', desc))
            has_numbers = bool(re.search(r'\d+', desc))
            
            if not has_percentage and len(desc) > 100:
                weaknesses.append(Weakness(
                    type="missing_metrics",
                    severity="medium",
                    description=f"Experiencia {i+1} carece de métricas cuantificables",
                    location=f"experience[{i}]",
                    suggestion="Añade porcentajes, números o montos: 'Aumenté ventas un 150%'"
                ))
        
        return weaknesses
    
    def _check_passive_language(self, cv_data: Dict) -> List[Weakness]:
        """Detecta uso de lenguaje pasivo."""
        weaknesses = []
        
        for i, exp in enumerate(cv_data.get("experience", [])):
            desc = exp.get("description", "").lower()
            
            passive_count = sum(1 for verb in self.PASSIVE_VERBS if verb in desc)
            strong_count = sum(1 for verb in self.STRONG_VERBS if verb in desc)
            
            if passive_count > strong_count:
                weaknesses.append(Weakness(
                    type="passive_language",
                    severity="medium",
                    description=f"Uso excesivo de lenguaje pasivo en experiencia {i+1}",
                    location=f"experience[{i}]",
                    suggestion="Usa verbos de acción: 'Lideré', 'Desarrollé', 'Implementé'"
                ))
        
        return weaknesses
    
    def _check_buzzwords(self, cv_data: Dict) -> List[Weakness]:
        """Detecta palabras vacías sin sustento."""
        weaknesses = []
        text = cv_data.get("raw_text", "").lower()
        
        found_buzzwords = [w for w in self.BUZZWORDS if w in text]
        
        if len(found_buzzwords) > 3:
            weaknesses.append(Weakness(
                type="buzzwords",
                severity="low",
                description=f"Palabras vacías detectadas: {', '.join(found_buzzwords[:5])}",
                location="global",
                suggestion="Reemplaza con ejemplos concretos de tus logros"
            ))
        
        return weaknesses
    
    def _check_keywords(self, cv_data: Dict) -> List[Weakness]:
        """Verifica presencia de keywords del sector."""
        # Simplificado - en producción usaría análisis de ofertas
        weaknesses = []
        
        tech_skills = cv_data.get("skills", {}).get("technical", [])
        if len(tech_skills) < 5:
            weaknesses.append(Weakness(
                type="few_skills",
                severity="high",
                description=f"Solo {len(tech_skills)} skills técnicas listadas",
                location="skills",
                suggestion="Añade al menos 10-15 skills relevantes para tu sector"
            ))
        
        return weaknesses
    
    def _check_length(self, cv_data: Dict) -> List[Weakness]:
        """Verifica longitud apropiada del CV."""
        weaknesses = []
        text = cv_data.get("raw_text", "")
        
        word_count = len(text.split())
        
        if word_count > 800:
            weaknesses.append(Weakness(
                type="too_long",
                severity="medium",
                description=f"CV muy largo ({word_count} palabras). Ideal: 400-600",
                location="global",
                suggestion="Condensa experiencias antiguas, elimina detalles irrelevantes"
            ))
        elif word_count < 200:
            weaknesses.append(Weakness(
                type="too_short",
                severity="high",
                description=f"CV muy corto ({word_count} palabras)",
                location="global",
                suggestion="Expande descripciones, añade más contexto a tus logros"
            ))
        
        return weaknesses
    
    def _check_structure(self, cv_data: Dict) -> List[Weakness]:
        """Verifica estructura completa del CV."""
        weaknesses = []
        
        required_sections = ["experience", "education", "skills"]
        for section in required_sections:
            if not cv_data.get(section):
                weaknesses.append(Weakness(
                    type="missing_section",
                    severity="high",
                    description=f"Falta sección: {section}",
                    location="structure",
                    suggestion=f"Añade sección de {section}"
                ))
        
        return weaknesses
```

```python
# src/cv_enhancer/cv_rewriter.py
"""Reescritura de CVs usando LLM local."""

import json
from typing import Dict, List
import requests


class CVRewriter:
    """Reescribe secciones de CV usando Ollama."""
    
    def __init__(self, model: str = "llama3.2", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.url = f"{ollama_url}/api/generate"
    
    def rewrite_profile(self, cv_data: Dict, job_target: str = "") -> str:
        """Reescribe el perfil profesional."""
        
        current_profile = cv_data.get("summary", "")
        experience = cv_data.get("experience", [])
        skills = cv_data.get("skills", {})
        
        prompt = f"""Eres un experto en redacción de CVs para el sector tech.
        
Reescribe el siguiente perfil profesional para que sea más impactante,
usando verbos de acción, métricas cuantificables y alineándolo con el puesto objetivo.

PUESTO OBJETIVO: {job_target or "No especificado"}

EXPERIENCIA ACTUAL:
{json.dumps(experience[:2], indent=2, ensure_ascii=False)}

SKILLS:
{json.dumps(skills, indent=2, ensure_ascii=False)}

PERFIL ACTUAL:
{current_profile or "No tiene perfil profesional"}

REGLAS:
1. Máximo 4 líneas
2. Usa verbos de acción al inicio
3. Incluye métricas si es posible
4. Menciona años de experiencia
5. Destaca especialización principal

PERFIL MEJORADO:"""
        
        return self._generate(prompt)
    
    def rewrite_experience(self, exp_entry: Dict, job_target: str = "") -> str:
        """Reescribe una entrada de experiencia."""
        
        prompt = f"""Reescribe la siguiente experiencia laboral para un CV profesional.

PUESTO: {exp_entry.get('title', '')}
EMPRESA: {exp_entry.get('company', '')}
DESCRIPCIÓN ACTUAL:
{exp_entry.get('description', '')}

REGLAS:
1. 3-5 viñetas máximo
2. Cada viñata empieza con verbo de acción fuerte
3. Incluye al menos 2 métricas cuantificables
4. Menciona tecnologías usadas
5. Enfoca en logros, no responsabilidades

DESCRIPCIÓN MEJORADA:"""
        
        return self._generate(prompt)
    
    def optimize_keywords(self, cv_data: Dict, job_description: str) -> List[str]:
        """Sugiere keywords faltantes para una oferta específica."""
        
        prompt = f"""Analiza el siguiente CV y oferta de empleo.
Identifica qué keywords importantes faltan en el CV.

CV SKILLS:
{json.dumps(cv_data.get('skills', {}), ensure_ascii=False)}

OFERTA:
{job_description[:1000]}

Lista solo las keywords faltantes más importantes, una por línea:"""
        
        response = self._generate(prompt)
        return [k.strip() for k in response.split('\n') if k.strip()]
    
    def _generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Genera texto usando Ollama."""
        
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": 500
                }
            }
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code}"
```

---

## 5. Ejercicios

### 🟢 Básico
1. Detectar debilidades en 3 CVs de ejemplo
2. Reescribir un perfil profesional con el sistema

### 🟡 Intermedio
3. Implementar detección de métricas con regex avanzado
4. Crear prompt template personalizable por sector

### 🔴 Avanzado
5. Fine-tuning de modelo local para reescritura de CVs
6. Sistema de A/B testing de versiones de CV

---

**[⬅️ Módulo 5](05-matching.md) | [➡️ Módulo 7](07-cartas-presentacion.md)**
```

---
