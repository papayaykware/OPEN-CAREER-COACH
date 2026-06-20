# 🤖 MÓDULO 13: Evolución hacia Agentes IA

> **Duración estimada:** 8-10 horas | **Nivel:** Experto

---

## 1. Arquitectura Multi-Agente

```
┌─────────────────────────────────────────┐
│         COORDINADOR CENTRAL             │
│         (Orquestador)                   │
└──────────┬──────────┬──────────┬────────┘
           │          │          │
    ┌──────▼───┐ ┌───▼────┐ ┌──▼─────┐ ┌──▼─────┐
    │  ATS     │ │  CV    │ │Training│ │Interview│
    │  Agent   │ │  Agent │ │ Agent  │ │ Agent   │
    └────┬─────┘ └───┬────┘ └──┬─────┘ └──┬─────┘
         │           │         │          │
         └───────────┴─────────┴──────────┘
                    │
              ┌─────▼─────┐
              │  Tools    │
              │  APIs     │
              │  DBs      │
              └───────────┘
```

---

## 2. Implementación Base

```python
# src/agents/base_agent.py
"""Agente base para el sistema multiagente."""

from typing import Dict, List, Any
from dataclasses import dataclass
import requests


@dataclass
class AgentResponse:
    action: str
    result: Any
    confidence: float
    next_agent: Optional[str] = None


class BaseAgent:
    """Agente base con capacidades LLM."""
    
    def __init__(self, name: str, model: str = "llama3.2"):
        self.name = name
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.tools: Dict[str, callable] = {}
    
    def register_tool(self, name: str, func: callable):
        """Registra una herramienta disponible."""
        self.tools[name] = func
    
    def think(self, context: Dict, task: str) -> AgentResponse:
        """Razona sobre una tarea y decide acción."""
        
        prompt = f"""Eres el agente {self.name}. 
Tienes acceso a las siguientes herramientas: {list(self.tools.keys())}

CONTEXTO:
{context}

TAREA:
{task}

Decide qué herramienta usar o si necesitas información de otro agente.
Responde en formato JSON:
{{
    "action": "nombre_tool",
    "parameters": {{...}},
    "confidence": 0.9,
    "next_agent": null  // o nombre de agente si necesitas ayuda
}}"""
        
        response = self._generate(prompt)
        # Parsear respuesta y ejecutar
        return self._parse_and_execute(response)
    
    def _generate(self, prompt: str) -> str:
        """Genera con LLM."""
        response = requests.post(
            self.ollama_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "")
    
    def _parse_and_execute(self, response: str) -> AgentResponse:
        """Parsea respuesta y ejecuta acción."""
        # Implementar parsing JSON
        return AgentResponse(action="unknown", result=response, confidence=0.5)


# src/agents/coordinator.py
"""Coordinador de agentes especializados."""

from typing import Dict, List
from .base_agent import BaseAgent


class AgentCoordinator:
    """Coordina múltiples agentes especializados."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflow: List[str] = []
    
    def register_agent(self, name: str, agent: BaseAgent):
        """Registra un agente en el sistema."""
        self.agents[name] = agent
    
    def execute_workflow(self, task: str, context: Dict) -> Dict:
        """Ejecuta workflow multi-agente."""
        
        results = {}
        current_agent = self._select_initial_agent(task)
        
        while current_agent:
            agent = self.agents[current_agent]
            response = agent.think(context, task)
            
            results[current_agent] = response
            
            if response.next_agent and response.next_agent in self.agents:
                current_agent = response.next_agent
            else:
                break
        
        return results
    
    def _select_initial_agent(self, task: str) -> str:
        """Selecciona agente inicial según tarea."""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ["cv", "currículum", "resume"]):
            return "cv_agent"
        elif any(kw in task_lower for kw in ["oferta", "job", "empleo"]):
            return "ats_agent"
        elif any(kw in task_lower for kw in ["formación", "curso", "aprender"]):
            return "training_agent"
        elif any(kw in task_lower for kw in ["entrevista", "interview"]):
            return "interview_agent"
        
        return "cv_agent"  # Default
```

---

## 3. Agentes Especializados

```python
# src/agents/ats_agent.py
"""Agente especializado en análisis ATS."""

from .base_agent import BaseAgent


class ATSAgent(BaseAgent):
    """Analiza compatibilidad ATS y da recomendaciones."""
    
    def __init__(self):
        super().__init__("ATS_Agent")
    
    def analyze_ats_compatibility(self, cv_data: Dict, job_data: Dict) -> Dict:
        """Analiza compatibilidad con sistemas ATS."""
        
        # Implementar análisis detallado
        return {
            "ats_score": 0.0,
            "keyword_match": [],
            "format_issues": [],
            "recommendations": []
        }


# src/agents/cv_agent.py
"""Agente especializado en optimización de CV."""

from .base_agent import BaseAgent


class CVAgent(BaseAgent):
    """Optimiza y mejora currículums."""
    
    def __init__(self):
        super().__init__("CV_Agent")
    
    def optimize_cv(self, cv_data: Dict, target_job: Dict = None) -> Dict:
        """Optimiza CV para objetivo específico."""
        return cv_data


# src/agents/interview_agent.py
"""Agente para preparación de entrevistas."""

from .base_agent import BaseAgent


class InterviewAgent(BaseAgent):
    """Prepara candidatos para entrevistas."""
    
    def __init__(self):
        super().__init__("Interview_Agent")
    
    def generate_questions(self, cv_data: Dict, job_data: Dict) -> List[str]:
        """Genera preguntas de entrevista personalizadas."""
        return []
    
    def evaluate_answer(self, question: str, answer: str) -> Dict:
        """Evalúa respuesta de entrevista."""
        return {}
```

---

## 4. Ejercicios

### 🟢 Básico
1. Implementar comunicación entre 2 agentes
2. Crear workflow simple: CV → Matching → Recomendación

### 🟡 Intermedio
3. Implementar memoria compartida entre agentes
4. Sistema de votación multi-agente para decisiones

### 🔴 Avanzado
5. Integrar con LangGraph para workflows complejos
6. Implementar aprendizaje por refuerzo entre agentes

---

**[⬅️ Módulo 12](12-despliegue.md) | [Volver al README](../README.md)**
```

---

