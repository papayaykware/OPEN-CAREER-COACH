
# Generar MÓDULO 5: Matching Inteligente

> **Duración estimada:** 6-8 horas | **Nivel:** Intermedio-Avanzado

---

## 1. Introducción

Este módulo construye el corazón del sistema: el motor de matching que compara currículums con ofertas de empleo usando embeddings, similitud semántica y análisis de brechas.

---

## 2. Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Generar embeddings de CVs y ofertas
- ✅ Calcular similitud semántica con múltiples métricas
- ✅ Implementar ranking de candidatos/ofertas
- ✅ Calcular compatibilidad ATS
- ✅ Realizar análisis de brechas (gap analysis)
- ✅ Generar scores desglosados por categoría

---

## 3. Fundamentos Teóricos

### 3.1 Embeddings para Matching

Los **embeddings** transforman texto en vectores numéricos donde la proximidad representa similitud semántica.

```
CV: "Desarrollador Python con 5 años de experiencia en Django y AWS"
    ↓ Embedding
    [0.23, -0.87, 0.15, ..., 0.91]  (768D)

Oferta: "Buscamos Python Developer con experiencia en Django y cloud AWS"
    ↓ Embedding
    [0.24, -0.86, 0.14, ..., 0.90]  (768D)

Similitud = 0.92  (Muy alta compatibilidad)
```

### 3.2 Métricas de Similitud

| Métrica | Fórmula | Uso | Rango |
|---------|---------|-----|-------|
| **Coseno** | (A·B)/(||A||×||B||) | Similitud direccional | [-1, 1] |
| **Euclídea** | √(Σ(Ai-Bi)²) | Distancia absoluta | [0, ∞) |
| **Manhattan** | Σ\|Ai-Bi\| | Distancia en grid | [0, ∞) |
| **Jaccard** | \|A∩B\|/\|A∪B\| | Sets binarios | [0, 1] |
| **Dot Product** | Σ(Ai×Bi) | Considera magnitud | (-∞, ∞) |

### 3.3 Matching Multi-Nivel

```
Compatibilidad Global
       │
       ├── Compatibilidad Técnica (40%)
       │      ├── Skills matching (60%)
       │      ├── Tech stack alignment (30%)
       │      └── Certifications (10%)
       │
       ├── Compatibilidad Competencial (30%)
       │      ├── Soft skills (50%)
       │      ├── Experience level (30%)
       │      └── Education fit (20%)
       │
       └── Compatibilidad Contextual (30%)
              ├── Location/remote (40%)
              ├── Salary alignment (30%)
              ├── Language fit (20%)
              └── Employment type (10%)
```

### 3.4 ATS Matching

El **ATS Matching** simula cómo un sistema ATS tradicional evaluaría el CV:

```
ATS Score = Σ(palabras_clave_encontradas / palabras_clave_totales) × peso_keyword
```

**Problema:** Los ATS tradicionales penalizan sinónimos.
**Solución:** Usar embeddings para matching semántico + keyword matching.

### 3.5 Gap Analysis

El **análisis de brechas** identifica qué falta al candidato:

```
Gap = {skill_requerido} - {skill_del_candidato}

Ejemplo:
  Requerido: {Python, Django, AWS, Docker, Kubernetes}
  Candidato: {Python, Django, AWS}
  
  Gap: {Docker, Kubernetes}
  
  Gap Score = 2/5 = 0.4 (falta el 40% de skills)
```

---

## 4. Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                   MATCHING ENGINE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐                         │
│  │     CV      │    │    Oferta   │                         │
│  │  (JSON)     │    │   (JSON)    │                         │
│  └──────┬──────┘    └──────┬──────┘                         │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              EMBEDDING GENERATOR                    │    │
│  │                                                     │    │
│  │  CV Text  ──▶ Sentence Transformers ──▶  Vector    │    │
│  │  Job Text ──▶   (nomic-embed-text)  ──▶  Vector    │    │
│  │                                                     │    │
│  │  Skills CV ──▶ One-hot / TF-IDF ──▶  Vector        │    │
│  │  Skills Job ──▶                   ──▶  Vector      │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              SIMILARITY CALCULATOR                  │    │
│  │                                                     │    │
│  │  Semantic Similarity  ──▶  Cosine(Embedding_CV,    │    │
│  │                                    Embedding_Job)   │    │
│  │                                                     │    │
│  │  Skill Similarity   ──▶  Jaccard(Skills_CV,        │    │
│  │                                    Skills_Job)      │    │
│  │                                                     │    │
│  │  Experience Match   ──▶  1 - |Exp_CV - Exp_Job|/   │    │
│  │                         max(Exp_CV, Exp_Job)        │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              SCORE AGGREGATOR                       │    │
│  │                                                     │    │
│  │  Global Score = w1×Tech + w2×Competencial +         │    │
│  │                 w3×Contextual + w4×ATS              │    │
│  │                                                     │    │
│  │  Weights: w1=0.35, w2=0.25, w3=0.20, w4=0.20        │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              GAP ANALYZER                           │    │
│  │                                                     │    │
│  │  Missing Skills = Required - Candidate              │    │
│  │  Missing Certs  = Required - Candidate              │    │
│  │  Experience Gap = Required - Candidate              │    │
│  │  Education Gap  = Required - Candidate              │    │
│  │                                                     │    │
│  │  Priority = f(rarity, demand, learning_curve)       │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              OUTPUT                                  │   │
│  │                                                      │   │
│  │  {                                                   │   │
│  │    "global_score": 0.78,                             │   │
│  │    "technical_score": 0.85,                          │   │
│  │    "competencial_score": 0.72,                       │   │
│  │    "contextual_score": 0.65,                         │   │
│  │    "ats_score": 0.90,                                │   │
│  │    "gaps": {                                         │   │
│  │      "missing_skills": ["Docker", "Kubernetes"],     │   │
│  │      "missing_certs": ["AWS Solutions Architect"],   │   │
│  │      "experience_gap": 0,                            │   │
│  │      "education_gap": 0                              │   │
│  │    },                                                │   │
│  │    "recommendations": [...]                          │   │
│  │  }                                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Implementación (Código)

### 5.1 Generador de Embeddings

```python
# src/matching/embeddings.py
"""Generación de embeddings para CVs y ofertas."""

import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Genera embeddings semánticos para texto de CVs y ofertas."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Inicializa el generador de embeddings.
        
        Args:
            model_name: Modelo de Sentence Transformers
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def generate(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Genera embeddings para uno o más textos.
        
        Args:
            texts: Texto o lista de textos
            
        Returns:
            Array numpy de embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization
        )
        
        return embeddings
    
    def generate_cv_embedding(self, cv_data: dict) -> np.ndarray:
        """Genera embedding combinado para un CV.
        
        Combina: experiencia + skills + educación
        """
        parts = []
        
        # Experiencia
        if cv_data.get("experience"):
            exp_texts = [
                f"{exp.get('title', '')} {exp.get('company', '')} {exp.get('description', '')}"
                for exp in cv_data["experience"]
            ]
            parts.extend(exp_texts)
        
        # Skills
        if cv_data.get("skills"):
            skills = cv_data["skills"]
            if isinstance(skills, dict):
                tech_skills = skills.get("technical", [])
                soft_skills = skills.get("soft", [])
                parts.append(f"Technical skills: {', '.join(tech_skills)}")
                parts.append(f"Soft skills: {', '.join(soft_skills)}")
            else:
                parts.append(f"Skills: {', '.join(skills)}")
        
        # Educación
        if cv_data.get("education"):
            edu_texts = [
                f"{edu.get('degree', '')} {edu.get('institution', '')}"
                for edu in cv_data["education"]
            ]
            parts.extend(edu_texts)
        
        # Generar embedding del texto combinado
        combined_text = " ".join(parts)
        return self.generate(combined_text)
    
    def generate_job_embedding(self, job_data: dict) -> np.ndarray:
        """Genera embedding combinado para una oferta."""
        parts = []
        
        # Título y descripción
        parts.append(job_data.get("title", ""))
        parts.append(job_data.get("description", ""))
        
        # Responsabilidades
        if job_data.get("responsibilities"):
            parts.extend(job_data["responsibilities"])
        
        # Skills requeridos
        if job_data.get("required_skills"):
            skills = job_data["required_skills"]
            if isinstance(skills, list) and len(skills) > 0:
                if isinstance(skills[0], dict):
                    skill_names = [s.get("skill", "") for s in skills]
                else:
                    skill_names = skills
                parts.append(f"Required skills: {', '.join(skill_names)}")
        
        # Soft skills
        if job_data.get("soft_skills"):
            parts.append(f"Soft skills: {', '.join(job_data['soft_skills'])}")
        
        combined_text = " ".join(parts)
        return self.generate(combined_text)
```

### 5.2 Calculador de Similitud

```python
# src/matching/similarity.py
"""Cálculo de similitud entre CVs y ofertas."""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from .embeddings import EmbeddingGenerator


@dataclass
class MatchResult:
    """Resultado completo de matching."""
    global_score: float
    technical_score: float
    competencial_score: float
    contextual_score: float
    ats_score: float
    semantic_similarity: float
    skill_similarity: float
    experience_match: float
    gaps: Dict[str, List[str]]
    recommendations: List[str]


class SimilarityCalculator:
    """Calcula similitud entre CVs y ofertas usando múltiples métricas."""
    
    def __init__(self, embedding_generator: Optional[EmbeddingGenerator] = None):
        self.embedder = embedding_generator or EmbeddingGenerator()
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula similitud coseno entre dos vectores.
        
        Args:
            vec1: Vector 1 (normalizado)
            vec2: Vector 2 (normalizado)
            
        Returns:
            Similitud coseno en [-1, 1]
        """
        # Si ya están normalizados, dot product = cosine similarity
        return float(np.dot(vec1.flatten(), vec2.flatten()))
    
    def euclidean_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula distancia euclídea."""
        return float(np.linalg.norm(vec1 - vec2))
    
    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calcula similitud de Jaccard entre dos sets.
        
        J(A,B) = |A ∩ B| / |A ∪ B|
        """
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def skill_similarity(
        self,
        cv_skills: List[str],
        job_skills: List[Union[str, dict]]
    ) -> Tuple[float, List[str], List[str]]:
        """Calcula similitud de skills con análisis de brechas.
        
        Args:
            cv_skills: Lista de skills del candidato
            job_skills: Lista de skills requeridos (str o dict con "skill")
            
        Returns:
            (score, matched_skills, missing_skills)
        """
        # Normalizar skills del CV
        cv_skills_set = set(s.lower().strip() for s in cv_skills)
        
        # Normalizar skills de la oferta
        job_skills_set = set()
        job_skills_list = []
        
        for skill in job_skills:
            if isinstance(skill, dict):
                skill_name = skill.get("skill", "").lower().strip()
            else:
                skill_name = skill.lower().strip()
            
            job_skills_set.add(skill_name)
            job_skills_list.append(skill_name)
        
        # Calcular coincidencias
        matched = cv_skills_set & job_skills_set
        missing = job_skills_set - cv_skills_set
        
        # Score ponderado
        if job_skills_set:
            score = len(matched) / len(job_skills_set)
        else:
            score = 0.0
        
        return score, list(matched), list(missing)
    
    def experience_match(
        self,
        cv_years: float,
        job_years: Optional[float],
        job_range: Optional[Tuple[int, int]] = None
    ) -> float:
        """Calcula match de experiencia.
        
        Args:
            cv_years: Años de experiencia del candidato
            job_years: Años mínimos requeridos
            job_range: Rango (min, max) requerido
            
        Returns:
            Score de match [0, 1]
        """
        if job_range:
            min_req, max_req = job_range
            if cv_years >= min_req:
                if cv_years <= max_req * 1.5:  # Tolerancia para sobre-cualificación
                    return 1.0
                else:
                    return 0.8  # Sobre-cualificado
            else:
                return max(0, cv_years / min_req)
        
        elif job_years is not None:
            if cv_years >= job_years:
                return 1.0
            else:
                return max(0, cv_years / job_years)
        
        return 0.5  # Sin requisito especificado
```

### 5.3 Motor de Matching

```python
# src/matching/ranking.py
"""Motor de matching completo CV-Oferta."""

import numpy as np
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

from .embeddings import EmbeddingGenerator
from .similarity import SimilarityCalculator, MatchResult


@dataclass
class WeightConfig:
    """Configuración de pesos para scoring."""
    technical: float = 0.35
    competencial: float = 0.25
    contextual: float = 0.20
    ats: float = 0.20


class CVJobMatcher:
    """Motor principal de matching entre CVs y ofertas."""
    
    def __init__(
        self,
        weights: Optional[WeightConfig] = None,
        similarity_threshold: float = 0.5
    ):
        self.embedder = EmbeddingGenerator()
        self.similarity = SimilarityCalculator(self.embedder)
        self.weights = weights or WeightConfig()
        self.threshold = similarity_threshold
    
    def calculate_match(
        self,
        cv_data: Dict,
        job_data: Dict
    ) -> MatchResult:
        """Calcula matching completo entre CV y oferta.
        
        Args:
            cv_data: Datos estructurados del CV
            job_data: Datos estructurados de la oferta
            
        Returns:
            MatchResult con scores y análisis
        """
        # 1. Similitud semántica (embeddings)
        cv_embedding = self.embedder.generate_cv_embedding(cv_data)
        job_embedding = self.embedder.generate_job_embedding(job_data)
        semantic_sim = self.similarity.cosine_similarity(cv_embedding, job_embedding)
        
        # 2. Similitud de skills
        cv_skills = self._extract_cv_skills(cv_data)
        job_skills = job_data.get("required_skills", [])
        skill_sim, matched_skills, missing_skills = self.similarity.skill_similarity(
            cv_skills, job_skills
        )
        
        # 3. Match de experiencia
        cv_exp = cv_data.get("total_experience_years", 0)
        job_exp = job_data.get("experience_years")
        job_range = job_data.get("experience_range")
        exp_match = self.similarity.experience_match(cv_exp, job_exp, job_range)
        
        # 4. Score técnico
        technical_score = self._calculate_technical_score(
            semantic_sim, skill_sim, exp_match, matched_skills, job_skills
        )
        
        # 5. Score competencial
        competencial_score = self._calculate_competencial_score(cv_data, job_data)
        
        # 6. Score contextual
        contextual_score = self._calculate_contextual_score(cv_data, job_data)
        
        # 7. Score ATS
        ats_score = self._calculate_ats_score(cv_data, job_data)
        
        # 8. Score global
        global_score = (
            self.weights.technical * technical_score +
            self.weights.competencial * competencial_score +
            self.weights.contextual * contextual_score +
            self.weights.ats * ats_score
        )
        
        # 9. Análisis de brechas
        gaps = self._analyze_gaps(cv_data, job_data, missing_skills)
        
        # 10. Recomendaciones
        recommendations = self._generate_recommendations(gaps, cv_data, job_data)
        
        return MatchResult(
            global_score=round(global_score, 3),
            technical_score=round(technical_score, 3),
            competencial_score=round(competencial_score, 3),
            contextual_score=round(contextual_score, 3),
            ats_score=round(ats_score, 3),
            semantic_similarity=round(semantic_sim, 3),
            skill_similarity=round(skill_sim, 3),
            experience_match=round(exp_match, 3),
            gaps=gaps,
            recommendations=recommendations
        )
    
    def rank_jobs(
        self,
        cv_data: Dict,
        jobs: List[Dict],
        top_k: int = 10
    ) -> List[Dict]:
        """Rankea ofertas por compatibilidad con un CV.
        
        Args:
            cv_data: Datos del CV
            jobs: Lista de ofertas
            top_k: Número de resultados a retornar
            
        Returns:
            Lista de ofertas rankeadas con scores
        """
        results = []
        
        for job in jobs:
            match = self.calculate_match(cv_data, job)
            results.append({
                "job": job,
                "match": match
            })
        
        # Ordenar por score global descendente
        results.sort(key=lambda x: x["match"].global_score, reverse=True)
        
        return results[:top_k]
    
    def _extract_cv_skills(self, cv_data: Dict) -> List[str]:
        """Extrae lista plana de skills del CV."""
        skills = []
        
        cv_skills = cv_data.get("skills", {})
        if isinstance(cv_skills, dict):
            skills.extend(cv_skills.get("technical", []))
            skills.extend(cv_skills.get("soft", []))
        elif isinstance(cv_skills, list):
            skills.extend(cv_skills)
        
        # Añadir skills inferidas de experiencia
        for exp in cv_data.get("experience", []):
            desc = exp.get("description", "").lower()
            # Aquí se podría usar NER o LLM para extraer más skills
        
        return skills
    
    def _calculate_technical_score(
        self,
        semantic_sim: float,
        skill_sim: float,
        exp_match: float,
        matched_skills: List[str],
        job_skills: List
    ) -> float:
        """Calcula score técnico ponderado."""
        # Ajustar pesos según importancia
        w_semantic = 0.30
        w_skills = 0.40
        w_experience = 0.20
        w_certs = 0.10
        
        # Bonus por skills obligatorios
        required_count = sum(1 for s in job_skills if isinstance(s, dict) and s.get("required", True))
        if required_count > 0:
            matched_required = sum(1 for s in matched_skills if any(
                isinstance(js, dict) and js.get("skill", "").lower() == s and js.get("required", True)
                for js in job_skills
            ))
            required_ratio = matched_required / required_count
        else:
            required_ratio = skill_sim
        
        score = (
            w_semantic * semantic_sim +
            w_skills * required_ratio +
            w_experience * exp_match +
            w_certs * 0.5  # Placeholder para certificaciones
        )
        
        return min(1.0, score)
    
    def _calculate_competencial_score(self, cv_data: Dict, job_data: Dict) -> float:
        """Calcula score competencial."""
        scores = []
        
        # Soft skills
        cv_soft = set(s.lower() for s in cv_data.get("skills", {}).get("soft", []))
        job_soft = set(s.lower() for s in job_data.get("soft_skills", []))
        
        if job_soft:
            soft_match = len(cv_soft & job_soft) / len(job_soft)
            scores.append(soft_match)
        
        # Educación
        cv_edu = cv_data.get("education", [])
        job_edu = job_data.get("education", [])
        if job_edu:
            # Simplificación: si tiene educación, score base
            edu_score = 0.7 if cv_edu else 0.3
            scores.append(edu_score)
        
        # Idiomas
        cv_langs = {l.get("language", "").lower() for l in cv_data.get("languages", [])}
        job_langs = {l.get("language", "").lower() for l in job_data.get("languages", [])}
        
        if job_langs:
            lang_match = len(cv_langs & job_langs) / len(job_langs)
            scores.append(lang_match)
        
        return np.mean(scores) if scores else 0.5
    
    def _calculate_contextual_score(self, cv_data: Dict, job_data: Dict) -> float:
        """Calcula score contextual."""
        scores = []
        
        # Ubicación / Remoto
        job_remote = job_data.get("remote_policy", "unknown")
        if job_remote in ["remote", "hybrid"]:
            scores.append(0.9)  # Alta compatibilidad
        else:
            scores.append(0.6)
        
        # Tipo de empleo
        job_type = job_data.get("employment_type", "full-time")
        scores.append(0.8)  # Asumir compatible
        
        # Salario (si disponible)
        job_salary = job_data.get("salary_range")
        if job_salary:
            scores.append(0.7)  # Neutral sin info del candidato
        
        return np.mean(scores) if scores else 0.5
    
    def _calculate_ats_score(self, cv_data: Dict, job_data: Dict) -> float:
        """Calcula score de compatibilidad ATS."""
        # Extraer keywords de la oferta
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')}"
        job_text_lower = job_text.lower()
        
        # Palabras clave importantes (simplificado)
        keywords = set()
        for skill in job_data.get("required_skills", []):
            if isinstance(skill, dict):
                keywords.add(skill.get("skill", "").lower())
            else:
                keywords.add(skill.lower())
        
        # Contar presencia en CV
        cv_text = cv_data.get("raw_text", "").lower()
        matched = sum(1 for kw in keywords if kw in cv_text)
        
        if keywords:
            return matched / len(keywords)
        return 0.5
    
    def _analyze_gaps(
        self,
        cv_data: Dict,
        job_data: Dict,
        missing_skills: List[str]
    ) -> Dict[str, List[str]]:
        """Analiza brechas entre CV y oferta."""
        gaps = {
            "missing_skills": missing_skills,
            "missing_certs": [],
            "experience_gap": [],
            "education_gap": [],
            "language_gap": []
        }
        
        # Certificaciones
        cv_certs = set(c.lower() for c in cv_data.get("certifications", []))
        job_certs = set(c.lower() for c in job_data.get("certifications", []))
        gaps["missing_certs"] = list(job_certs - cv_certs)
        
        # Experiencia
        cv_exp = cv_data.get("total_experience_years", 0)
        job_exp = job_data.get("experience_years")
        if job_exp and cv_exp < job_exp:
            gaps["experience_gap"].append(f"Faltan {job_exp - cv_exp:.1f} años de experiencia")
        
        # Idiomas
        cv_langs = {l.get("language", "").lower() for l in cv_data.get("languages", [])}
        job_langs = {l.get("language", "").lower() for l in job_data.get("languages", [])}
        gaps["language_gap"] = list(job_langs - cv_langs)
        
        return gaps
    
    def _generate_recommendations(
        self,
        gaps: Dict,
        cv_data: Dict,
        job_data: Dict
    ) -> List[str]:
        """Genera recomendaciones basadas en brechas."""
        recommendations = []
        
        if gaps["missing_skills"]:
            skills_str = ", ".join(gaps["missing_skills"][:5])
            recommendations.append(
                f"Adquiere las siguientes skills: {skills_str}"
            )
        
        if gaps["missing_certs"]:
            certs_str = ", ".join(gaps["missing_certs"][:3])
            recommendations.append(
                f"Considera obtener: {certs_str}"
            )
        
        if gaps["experience_gap"]:
            recommendations.extend(gaps["experience_gap"])
        
        if gaps["language_gap"]:
            langs_str = ", ".join(gaps["language_gap"])
            recommendations.append(
                f"Mejora tu nivel de: {langs_str}"
            )
        
        if not recommendations:
            recommendations.append(
                "¡Excelente match! Tu perfil cumple con todos los requisitos principales."
            )
        
        return recommendations
```

---

## 6. Explicación Línea a Línea

### EmbeddingGenerator

| Línea | Explicación |
|-------|-------------|
| `normalize_embeddings=True` | Normaliza vectores a longitud 1 para cosine similarity eficiente |
| `convert_to_numpy=True` | Devuelve arrays numpy en lugar de tensores PyTorch |
| `combined_text = " ".join(parts)` | Concatena todas las secciones para embedding holístico |

### CVJobMatcher

| Línea | Explicación |
|-------|-------------|
| `round(global_score, 3)` | Redondea para legibilidad sin perder precisión |
| `min(1.0, score)` | Clampa score máximo a 1.0 |
| `np.mean(scores)` | Promedio simple de sub-scores |
| `results.sort(key=lambda x: x["match"].global_score, reverse=True)` | Ordena descendente por score |

---

## 7. Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| Score siempre alto | Embeddings no normalizados | Verificar `normalize_embeddings=True` |
| Skills no coinciden | Diferentes nombres ("JS" vs "JavaScript") | Crear taxonomy de sinónimos |
| Experiencia sobrevalorada | Candidato sobre-cualificado | Penalizar sobre-cualificación |
| Falso positivo | CV genérico coincide con todo | Añadir especificidad al embedding |
| Lento con muchos jobs | Recalcula embeddings cada vez | Cachear embeddings en vector DB |

---

## 8. Ejercicios

### 🟢 Nivel Básico

1. **Calcular** manualmente similitud coseno entre dos vectores de 5 dimensiones.
2. **Probar** el matcher con un CV y 3 ofertas reales.
3. **Ajustar** pesos y observar cómo cambian los rankings.

### 🟡 Nivel Intermedio

4. **Implementar** cache de embeddings usando pickle/JSON.
5. **Añadir** sinónimos para skills ("JS" = "JavaScript" = "ECMAScript").
6. **Crear** visualización de scores con matplotlib.

### 🔴 Nivel Avanzado

7. **Implementar** búsqueda aproximada con FAISS para millones de ofertas.
8. **Añadir** análisis de sentimiento a la descripción para detectar cultura tóxica.
9. **Crear** sistema de feedback para ajustar pesos con aprendizaje.

---

## 9. Reto Profesional

**Escenario:** Plataforma de empleo con 100,000 CVs y 50,000 ofertas activas.

**Entregable:**
- Sistema de matching en tiempo real (<200ms)
- Indexación con FAISS para búsqueda masiva
- API REST para matching batch y en tiempo real
- Dashboard de analytics de matching
- Sistema de feedback para mejora continua

---

**[⬅️ Módulo 4: Procesamiento de Ofertas](04-procesamiento-ofertas.md) | [➡️ Módulo 6: Mejorador de CV](06-mejorador-cv.md)**
'''

