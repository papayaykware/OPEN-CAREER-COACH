# 🎓 MÓDULO 8: Recomendador de Formación

> **Duración estimada:** 4-6 horas | **Nivel:** Intermedio

---

## 1. Introducción

Sistema que identifica brechas de habilidades entre un CV y ofertas objetivo, recomienda cursos/certificaciones y genera roadmaps profesionales.

---

## 2. Arquitectura

```
Brechas Identificadas
       │
       ▼
┌─────────────────┐
│  Priorización   │───▶ Impacto × Urgencia × Dificultad
│                 │
│ • Alta demanda  │
│ • Salario       │
│ • Tiempo        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Recomendación  │───▶ Cursos, certificaciones, proyectos
│                 │
│ • Plataformas   │
│ • Gratuitos     │
│ • Premium       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Roadmap      │───▶ Timeline visual de 6-12-24 meses
│                 │
│ • Fases         │
│ • Milestones    │
│ • Recursos      │
└─────────────────┘
```

---

## 3. Implementación

```python
# src/training_recommender/gap_identifier.py
"""Identificación de brechas de habilidades."""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class SkillGap:
    skill: str
    current_level: str
    target_level: str
    priority: str  # high, medium, low
    estimated_hours: int


class GapIdentifier:
    """Identifica brechas entre perfil actual y objetivo."""
    
    # Base de datos de skills con niveles típicos
    SKILL_LEVELS = {
        "python": {"junior": 100, "mid": 300, "senior": 500},
        "docker": {"junior": 40, "mid": 80, "senior": 150},
        "kubernetes": {"junior": 60, "mid": 120, "senior": 250},
        # ... más skills
    }
    
    def identify_gaps(
        self,
        cv_data: Dict,
        target_job: Dict
    ) -> List[SkillGap]:
        """Identifica todas las brechas."""
        gaps = []
        
        cv_skills = {s.lower() for s in cv_data.get("skills", {}).get("technical", [])}
        
        for req_skill in target_job.get("required_skills", []):
            skill_name = req_skill.get("skill", "").lower() if isinstance(req_skill, dict) else req_skill.lower()
            
            if skill_name not in cv_skills:
                # Calcular prioridad
                priority = self._calculate_priority(req_skill, target_job)
                hours = self._estimate_learning_hours(skill_name)
                
                gaps.append(SkillGap(
                    skill=skill_name,
                    current_level="none",
                    target_level="proficient",
                    priority=priority,
                    estimated_hours=hours
                ))
        
        return sorted(gaps, key=lambda x: x.priority != "high")
    
    def _calculate_priority(self, skill, job_data: Dict) -> str:
        """Calcula prioridad de una brecha."""
        if isinstance(skill, dict):
            weight = skill.get("weight", 0.5)
            required = skill.get("required", False)
        else:
            weight = 0.5
            required = False
        
        if required and weight >= 0.8:
            return "high"
        elif weight >= 0.5:
            return "medium"
        return "low"
    
    def _estimate_learning_hours(self, skill: str) -> int:
        """Estima horas de aprendizaje."""
        return self.SKILL_LEVELS.get(skill, {}).get("mid", 100)


# src/training_recommender/roadmap_generator.py
"""Generador de roadmaps profesionales."""

from typing import Dict, List
import json


class RoadmapGenerator:
    """Genera roadmaps de desarrollo profesional."""
    
    # Base de datos de recursos de aprendizaje
    RESOURCES = {
        "python": [
            {"name": "Python for Everybody (Coursera)", "type": "course", "hours": 40, "cost": "free"},
            {"name": "Real Python", "type": "tutorial", "hours": 100, "cost": "subscription"},
        ],
        "docker": [
            {"name": "Docker Mastery (Udemy)", "type": "course", "hours": 20, "cost": "paid"},
            {"name": "Docker Docs", "type": "documentation", "hours": 10, "cost": "free"},
        ],
        # ... más recursos
    }
    
    def generate_roadmap(
        self,
        gaps: List,
        timeframe_months: int = 6,
        hours_per_week: int = 10
    ) -> Dict:
        """Genera roadmap personalizado."""
        
        total_hours = timeframe_months * 4 * hours_per_week
        available_hours = total_hours
        
        phases = []
        current_phase = []
        phase_hours = 0
        phase_limit = total_hours // 3  # 3 fases
        
        for gap in gaps:
            resources = self.RESOURCES.get(gap.skill, [])
            
            for resource in resources[:2]:  # Top 2 recursos
                if available_hours <= 0:
                    break
                
                hours = min(resource["hours"], available_hours)
                
                item = {
                    "skill": gap.skill,
                    "resource": resource["name"],
                    "type": resource["type"],
                    "hours": hours,
                    "cost": resource["cost"],
                    "priority": gap.priority
                }
                
                current_phase.append(item)
                phase_hours += hours
                available_hours -= hours
                
                if phase_hours >= phase_limit:
                    phases.append(current_phase)
                    current_phase = []
                    phase_hours = 0
        
        if current_phase:
            phases.append(current_phase)
        
        return {
            "timeframe_months": timeframe_months,
            "hours_per_week": hours_per_week,
            "total_hours": total_hours,
            "phases": phases,
            "milestones": self._generate_milestones(phases)
        }
    
    def _generate_milestones(self, phases: List[List[Dict]]) -> List[Dict]:
        """Genera milestones del roadmap."""
        milestones = []
        
        for i, phase in enumerate(phases):
            skills = list(set(item["skill"] for item in phase))
            milestones.append({
                "phase": i + 1,
                "title": f"Fase {i + 1}: {', '.join(skills[:3])}",
                "skills": skills,
                "estimated_weeks": sum(item["hours"] for item in phase) // 10
            })
        
        return milestones
```

---

## 4. Ejercicios

### 🟢 Básico
1. Identificar gaps para un perfil junior vs oferta senior
2. Generar roadmap de 6 meses para un caso real

### 🟡 Intermedio
3. Integrar con APIs de plataformas (Coursera, Udemy)
4. Añadir estimación de ROI salarial por certificación

### 🔴 Avanzado
5. Sistema de tracking de progreso del usuario
6. Recomendaciones adaptativas basadas en progreso

---

**[⬅️ Módulo 7](07-cartas-presentacion.md) | [➡️ Módulo 9](09-sistema-rag.md)**
```

---


