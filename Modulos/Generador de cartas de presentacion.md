# 📝 MÓDULO 7: Generador de Cartas de Presentación

> **Duración estimada:** 4-5 horas | **Nivel:** Intermedio

---

## 1. Introducción

Sistema para generar cartas de presentación personalizadas usando LLMs locales, con múltiples estilos y adaptación a ofertas específicas.

---

## 2. Tipos de Carta

| Tipo | Uso | Tono |
|------|-----|------|
| **Clásica** | Sectores tradicionales | Formal, estructurada |
| **Técnica** | Tech/IT | Directa, enfocada en skills |
| **Ejecutiva** | C-level | Estratégica, visionaria |

---

## 3. Implementación

```python
# src/cover_letter/generator.py
"""Generador de cartas de presentación."""

from typing import Dict, Optional
import requests


class CoverLetterGenerator:
    """Genera cartas de presentación personalizadas."""
    
    TEMPLATES = {
        "classic": """Estimado/a {hiring_manager}:

Me dirijo a usted en relación con la posición de {job_title} en {company}. 
Con {years_experience} años de experiencia en {main_skill}, estoy convencido/a 
de que puedo aportar valor significativo a su equipo.

{body_paragraphs}

Quedo a su disposición para una entrevista en la que podamos 
discutir cómo puedo contribuir al éxito de {company}.

Atentamente,
{candidate_name}""",
        
        "technical": """Hi {hiring_manager},

I'm writing about the {job_title} role at {company}. 

{technical_highlights}

{body_paragraphs}

I've attached my CV and would love to discuss how my experience 
with {main_technologies} aligns with your team's needs.

Best,
{candidate_name}""",
        
        "executive": """Dear {hiring_manager},

The {job_title} position at {company} represents an exciting opportunity 
to drive {strategic_goal}. With my track record of {key_achievement}, 
I am uniquely positioned to deliver results.

{leadership_paragraphs}

I look forward to discussing how my strategic vision can accelerate 
{company}'s growth in {market_sector}.

Sincerely,
{candidate_name}"""
    }
    
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
    
    def generate(
        self,
        cv_data: Dict,
        job_data: Dict,
        style: str = "classic",
        hiring_manager: Optional[str] = None
    ) -> str:
        """Genera carta de presentación personalizada."""
        
        # Construir prompt según estilo
        prompt = self._build_prompt(cv_data, job_data, style, hiring_manager)
        
        # Generar con LLM
        return self._generate_text(prompt)
    
    def _build_prompt(
        self,
        cv_data: Dict,
        job_data: Dict,
        style: str,
        hiring_manager: Optional[str]
    ) -> str:
        """Construye prompt para generación."""
        
        cv_summary = self._summarize_cv(cv_data)
        job_summary = self._summarize_job(job_data)
        
        return f"""Escribe una carta de presentación {style} para:

CANDIDATO:
{cv_summary}

OFERTA:
{job_summary}

ESTILO: {style}
DESTINATARIO: {hiring_manager or "Responsable de contratación"}

REGLAS:
- Máximo 300 palabras
- Menciona 2-3 logros específicos del candidato
- Conecta skills del candidato con requisitos de la oferta
- Muestra conocimiento de la empresa
- Cierra con call-to-action

CARTA:"""
    
    def _summarize_cv(self, cv_data: Dict) -> str:
        """Resume CV para el prompt."""
        parts = [
            f"Nombre: {cv_data.get('personal_info', {}).get('name', '')}",
            f"Experiencia: {cv_data.get('total_experience_years', 0)} años",
            f"Skills: {', '.join(cv_data.get('skills', {}).get('technical', [])[:5])}",
        ]
        return "\n".join(parts)
    
    def _summarize_job(self, job_data: Dict) -> str:
        """Resume oferta para el prompt."""
        parts = [
            f"Puesto: {job_data.get('title', '')}",
            f"Empresa: {job_data.get('company', '')}",
            f"Skills requeridos: {', '.join(s.get('skill', '') for s in job_data.get('required_skills', [])[:5])}",
        ]
        return "\n".join(parts)
    
    def _generate_text(self, prompt: str) -> str:
        """Genera texto con Ollama."""
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.8, "num_predict": 800}
            }
        )
        return response.json().get("response", "")
```

---

## 4. Ejercicios

### 🟢 Básico
1. Generar 3 cartas para la misma oferta con diferentes estilos
2. Comparar y elegir la más adecuada

### 🟡 Intermedio
3. Implementar sistema de puntuación de calidad de carta
4. Añadir detección de clichés y palabras vacías

### 🔴 Avanzado
5. Sistema de few-shot learning con ejemplos de cartas exitosas
6. A/B testing de cartas con métricas de respuesta

---

**[⬅️ Módulo 6](06-mejorador-cv.md) | [➡️ Módulo 8](08-recomendador-formacion.md)**
```

---
