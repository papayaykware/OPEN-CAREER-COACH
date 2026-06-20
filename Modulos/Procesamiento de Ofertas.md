#  MÓDULO 4: Procesamiento de Ofertas

> **Duración estimada:** 5-7 horas | **Nivel:** Intermedio

---

## 1. Introducción

Este módulo construye el sistema de extracción de información de ofertas de empleo. Aprenderás a parsear descripciones de puestos, identificar requisitos técnicos y blandos, y estructurar la información para comparación con CVs.

---

## 2. Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Extraer información estructurada de descripciones de empleo
- ✅ Identificar hard skills, soft skills y tecnologías
- ✅ Detectar años de experiencia requeridos
- ✅ Extraer certificaciones y requisitos de idiomas
- ✅ Generar representación estructurada compatible con CVs
- ✅ Calcular pesos de importancia por requisito

---

## 3. Fundamentos Teóricos

### 3.1 Estructura de una Oferta de Empleo

```
┌─────────────────────────────────────────────────────────┐
│              ESTRUCTURA TÍPICA DE OFERTA                │
├─────────────────────────────────────────────────────────┤
│  1. Título del puesto                                   │
│  2. Empresa / Ubicación / Modalidad                     │
│  3. Descripción general                                 │
│  4. Responsabilidades / Funciones                       │
│  5. Requisitos técnicos (hard skills)                   │
│  6. Requisitos personales (soft skills)                 │
│  7. Experiencia requerida                               │
│  8. Formación requerida                                 │
│  9. Certificaciones deseables                           │
│  10. Idiomas requeridos                                 │
│  11. Beneficios / Salario                               │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Tipos de Requisitos

| Tipo | Ejemplos | Detección |
|------|----------|-----------|
| **Hard Skills** | Python, AWS, Kubernetes, React | Diccionario + NER |
| **Soft Skills** | Liderazgo, comunicación, proactividad | NLP + LLM |
| **Tecnologías** | Docker, Terraform, Jenkins | Diccionario tech |
| **Certificaciones** | AWS Solutions Architect, PMP | Patrones regex |
| **Idiomas** | Inglés C1, Español nativo | NLP + regex |
| **Experiencia** | 3+ años, 5 años mínimo | Regex numérico |
| **Formación** | Grado en Informática, Máster | NER + keywords |

### 3.3 Ponderación de Requisitos

No todos los requisitos tienen la misma importancia:

```
Peso = f(tipo, frecuencia_en_texto, posición_en_lista, obligatoriedad)

Ejemplo:
- "Requisitos obligatorios" → peso 1.0
- "Se valorará" → peso 0.5
- "Nice to have" → peso 0.3
- Mencionado en título → peso 1.2
```

---

## 4. Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│            PIPELINE DE PROCESAMIENTO DE OFERTAS             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                            │
│  │   Input     │                                            │
│  │  Texto de   │                                            │
│  │   oferta    │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         PREPROCESAMIENTO                            │    │
│  │  • Normalización Unicode                            │    │
│  │  • Corrección de encoding                           │    │
│  │  • Detección de idioma                              │    │
│  │  • Eliminación de HTML/markdown                     │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         SEGMENTACIÓN DE SECCIONES                   │    │
│  │                                                     │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │    │
│  │  │Título   │ │Desc.     │ │Requisitos│ │Benefic│    │    │
│  │  │Empresa  │ │General   │ │Técnicos  │ │Salario│    │    │
│  │  │Ubicación│ │Funciones │ │Personales│         │    │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         EXTRACCIÓN DE REQUISITOS                    │    │
│  │                                                     │    │
│  │  ┌─────────────┐      ┌─────────────┐               │    │
│  │  │  Diccionario │     │     LLM      │              │    │
│  │  │   + Regex    │     │  (Ollama)    │              │    │
│  │  │              │     │              │              │    │
│  │  │ • Skills     │     │ • Soft skills│              │    │
│  │  │ • Tech stack │     │ • Responsab. │              │    │
│  │  │ • Certs      │     │ • Inferencia │              │    │
│  │  │ • Idiomas    │     │ • Contexto   │              │    │
│  │  └─────────────┘       └─────────────┘              │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         PONDERACIÓN Y ESTRUCTURACIÓN                │    │
│  │                                                     │    │
│  │  {                                                  │    │
│  │    "title": "Senior Python Developer",              │    │
│  │    "company": "TechCorp",                           │    │
│  │    "location": "Madrid (Híbrido)",                  │    │
│  │    "required_skills": [                             │    │
│  │      {"skill": "Python", "weight": 1.0, "required": true},   
│  │      {"skill": "Django", "weight": 0.8, "required": true},   
│  │      {"skill": "AWS", "weight": 0.6, "required": false}  │   
│  │    ],                                               │    │
│  │    "soft_skills": ["Liderazgo", "Comunicación"],    │    │
│  │    "experience_years": 5,                           │    │
│  │    "education": "Grado en Informática",             │    │
│  │    "certifications": ["AWS Solutions Architect"],   │    │
│  │    "languages": [{"language": "Inglés", "level": "C1"}]  │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Implementación (Código)

### 5.1 Parser de Ofertas

```python
# src/job_parser/job_scraper.py
"""Extracción de información de ofertas de empleo."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class SkillRequirement:
    """Requisito de habilidad con peso."""
    skill: str
    weight: float = 1.0
    required: bool = True
    category: str = "technical"  # technical, soft, language, certification


@dataclass
class JobOffer:
    """Oferta de empleo estructurada."""
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    responsibilities: List[str] = field(default_factory=list)
    required_skills: List[SkillRequirement] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    experience_years: Optional[int] = None
    experience_range: Optional[Tuple[int, int]] = None
    education: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[Dict[str, str]] = field(default_factory=list)
    salary_range: Optional[Tuple[float, float]] = None
    employment_type: str = ""  # full-time, part-time, contract
    remote_policy: str = ""  # remote, hybrid, on-site
    raw_text: str = ""


class JobParser:
    """Parser completo de ofertas de empleo."""
    
    # Diccionario de skills técnicas
    TECH_SKILLS = {
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "ruby", "php", "scala", "kotlin", "swift", "objective-c",
        "sql", "postgresql", "mysql", "mongodb", "redis", "cassandra", "dynamodb",
        "elasticsearch", "solr", "neo4j", "sqlite",
        "docker", "kubernetes", "openshift", "rancher",
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "terraform", "ansible", "puppet", "chef", "vagrant",
        "jenkins", "gitlab ci", "github actions", "circleci", "travis ci", "bamboo",
        "react", "vue", "vue.js", "angular", "svelte", "next.js", "nuxt",
        "nodejs", "node.js", "express", "django", "flask", "fastapi", "spring boot",
        "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "spark", "hadoop", "kafka", "airflow", "dbt", "snowflake",
        "tableau", "power bi", "looker", "qlik",
        "git", "svn", "mercurial",
        "linux", "ubuntu", "centos", "debian", "redhat",
        "nginx", "apache", "iis", "tomcat",
        "rest api", "graphql", "grpc", "soap", "websockets",
        "microservices", "serverless", "lambda", "event-driven",
        "ci/cd", "devops", "sre", "platform engineering",
        "agile", "scrum", "kanban", "safe",
        "machine learning", "deep learning", "nlp", "computer vision",
        "data science", "data engineering", "data analytics",
        "blockchain", "solidity", "web3", "smart contracts",
    }
    
    # Diccionario de soft skills
    SOFT_SKILLS = {
        "liderazgo", "leadership", "comunicación", "communication",
        "trabajo en equipo", "teamwork", "team player",
        "resolución de problemas", "problem solving",
        "pensamiento crítico", "critical thinking",
        "adaptabilidad", "adaptability", "flexibility", "flexible",
        "creatividad", "creativity", "innovation", "innovative",
        "gestión del tiempo", "time management",
        "empatía", "empathy",
        "negociación", "negotiation",
        "presentación", "presentation skills",
        "proactividad", "proactive", "self-starter",
        "autonomía", "autonomy", "self-motivated",
        "atención al detalle", "attention to detail",
        "gestión de proyectos", "project management",
        "análisis", "analytical thinking",
        "orientación a resultados", "results-oriented",
        "orientación al cliente", "customer-oriented",
    }
    
    # Patrones para experiencia
    EXPERIENCE_PATTERNS = [
        r'(?:minimum\\s+)?(?:(\\d+)\\+?\\s*(?:years?|años?)(?:\\s+of)?(?:\\s+experience)?)',
        r'(?:(\\d+)\\s*(?:-|to|a)\\s*(\\d+)\\s*(?:years?|años?))',
        r'(?:experiencia(?:\\s+mínima)?(?:\\s+de)?\\s+)(\\d+)\\s*(?:años?|years?)',
        r'(?:al\\s+menos\\s+)(\\d+)\\s*(?:años?|years?)',
    ]
    
    # Patrones para salario
    SALARY_PATTERNS = [
        r'(?:\\$|€|£)?\\s*(\\d{2,3}(?:,\\d{3})*)\\s*(?:-|to|a)\\s*(?:\\$|€|£)?\\s*(\\d{2,3}(?:,\\d{3})*)',
        r'(?:salary|rango|range)[^\\d]*(\\d{2,3}(?:,\\d{3})*)[^\\d]*(\\d{2,3}(?:,\\d{3})*)',
    ]
    
    def __init__(self):
        self.tech_skills_lower = {s.lower() for s in self.TECH_SKILLS}
        self.soft_skills_lower = {s.lower() for s in self.SOFT_SKILLS}
    
    def parse(self, text: str) -> JobOffer:
        """Parsea una oferta de empleo completa.
        
        Args:
            text: Texto completo de la oferta
            
        Returns:
            JobOffer estructurada
        """
        offer = JobOffer(raw_text=text)
        
        # Preprocesar
        clean_text = self._preprocess(text)
        
        # Extraer secciones
        sections = self._extract_sections(clean_text)
        
        # Extraer información básica
        offer.title = self._extract_title(clean_text, sections)
        offer.company = self._extract_company(clean_text)
        offer.location = self._extract_location(clean_text)
        
        # Extraer requisitos
        offer.required_skills = self._extract_skills(clean_text, sections)
        offer.soft_skills = self._extract_soft_skills(clean_text)
        
        # Extraer experiencia
        offer.experience_years, offer.experience_range = self._extract_experience(clean_text)
        
        # Extraer formación
        offer.education = self._extract_education(clean_text)
        
        # Extraer certificaciones
        offer.certifications = self._extract_certifications(clean_text)
        
        # Extraer idiomas
        offer.languages = self._extract_languages(clean_text)
        
        # Extraer salario
        offer.salary_range = self._extract_salary(clean_text)
        
        # Extraer tipo de empleo y modalidad
        offer.employment_type = self._extract_employment_type(clean_text)
        offer.remote_policy = self._extract_remote_policy(clean_text)
        
        return offer
    
    def _preprocess(self, text: str) -> str:
        """Limpia y normaliza el texto."""
        # Eliminar HTML
        text = re.sub(r'<[^>]+>', ' ', text)
        # Normalizar espacios
        text = re.sub(r'\\s+', ' ', text)
        # Normalizar Unicode
        text = text.replace("\\u2013", "-").replace("\\u2014", "-")
        text = text.replace("\\u2019", "'").replace("\\u2018", "'")
        return text.strip()
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extrae secciones principales de la oferta."""
        sections = {}
        
        section_patterns = {
            "description": [
                r'(?:descripción|description|about the role|sobre el puesto)[:\\s]*',
            ],
            "requirements": [
                r'(?:requisitos|requirements|what you need|qué necesitas|must have)[:\\s]*',
            ],
            "responsibilities": [
                r'(?:responsabilidades|responsibilities|what you will do|funciones)[:\\s]*',
            ],
            "benefits": [
                r'(?:beneficios|benefits|what we offer|qué ofrecemos)[:\\s]*',
            ],
        }
        
        lines = text.split("\\n")
        current_section = "header"
        
        for line in lines:
            line_lower = line.lower().strip()
            
            for section_name, patterns in section_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line_lower):
                        current_section = section_name
                        break
            
            if current_section not in sections:
                sections[current_section] = []
            sections[current_section].append(line)
        
        # Convertir listas a strings
        return {k: "\\n".join(v) for k, v in sections.items()}
    
    def _extract_title(self, text: str, sections: Dict[str, str]) -> str:
        """Extrae el título del puesto."""
        lines = text.split("\\n")[:5]  # Primeras líneas
        
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                # Heurística: título suele ser corto y contener palabras de puesto
                if any(kw in line.lower() for kw in [
                    "developer", "engineer", "manager", "analyst", "consultant",
                    "desarrollador", "ingeniero", "gerente", "analista", "consultor",
                    "lead", "senior", "junior", "architect", "arquitecto",
                ]):
                    return line
        
        return lines[0].strip() if lines else ""
    
    def _extract_company(self, text: str) -> str:
        """Extrae el nombre de la empresa."""
        # Buscar después de "en" o "at" cerca del título
        patterns = [
            r'(?:en|at|para|for)\\s+([A-Z][A-Za-z\\s&]+)(?:\\s*[.,;]|\\s*$)',
            r'^([A-Z][A-Za-z\\s&]+)(?:\\s*[-|])',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text[:500])
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_location(self, text: str) -> str:
        """Extrae ubicación."""
        patterns = [
            r'(?:ubicación|location|lugar|place)[:\\s]*([^\\n]+)',
            r'(?:remote|híbrido|hybrid|presencial|on-site)',
            r'(?:madrid|barcelona|valencia|sevilla|bilbao|remoto)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text[:1000], re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        return ""
    
    def _extract_skills(self, text: str, sections: Dict[str, str]) -> List[SkillRequirement]:
        """Extrae skills técnicas con pesos."""
        skills = []
        text_lower = text.lower()
        
        # Buscar en sección de requisitos primero
        req_text = sections.get("requirements", text)
        req_lower = req_text.lower()
        
        for skill in self.tech_skills_lower:
            # Buscar palabra completa
            pattern = r'\\b' + re.escape(skill) + r'\\b'
            
            if re.search(pattern, req_lower):
                # Determinar peso
                weight = self._calculate_skill_weight(skill, req_lower)
                required = self._is_required(skill, req_lower)
                
                skills.append(SkillRequirement(
                    skill=skill,
                    weight=weight,
                    required=required,
                    category="technical"
                ))
        
        return skills
    
    def _calculate_skill_weight(self, skill: str, text: str) -> float:
        """Calcula el peso de un skill basado en contexto."""
        weight = 0.5  # Base
        
        # Palabras que indican requisito obligatorio
        mandatory_keywords = ["requerido", "required", "obligatorio", "mandatory", "must have", "imprescindible"]
        # Palabras que indican deseable
        optional_keywords = ["deseable", "valorable", "nice to have", "plus", "preferible", "preferred"]
        
        # Buscar contexto alrededor del skill
        pattern = r'[^.]*\\b' + re.escape(skill) + r'\\b[^.]*'
        contexts = re.findall(pattern, text, re.IGNORECASE)
        
        for context in contexts:
            context_lower = context.lower()
            if any(kw in context_lower for kw in mandatory_keywords):
                weight = 1.0
                break
            elif any(kw in context_lower for kw in optional_keywords):
                weight = 0.3
            else:
                weight = 0.7
        
        return weight
    
    def _is_required(self, skill: str, text: str) -> bool:
        """Determina si un skill es obligatorio."""
        pattern = r'[^.]*\\b' + re.escape(skill) + r'\\b[^.]*'
        contexts = re.findall(pattern, text, re.IGNORECASE)
        
        optional_keywords = ["deseable", "valorable", "nice to have", "plus", "preferible"]
        
        for context in contexts:
            if any(kw in context.lower() for kw in optional_keywords):
                return False
        
        return True
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extrae soft skills."""
        found = []
        text_lower = text.lower()
        
        for skill in self.soft_skills_lower:
            pattern = r'\\b' + re.escape(skill) + r'\\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        
        return list(set(found))
    
    def _extract_experience(self, text: str) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Extrae años de experiencia requeridos."""
        text_lower = text.lower()
        
        for pattern in self.EXPERIENCE_PATTERNS:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    # Rango
                    try:
                        min_years = int(match[0])
                        max_years = int(match[1])
                        return None, (min_years, max_years)
                    except (ValueError, IndexError):
                        continue
                else:
                    # Años mínimos
                    try:
                        years = int(match)
                        return years, None
                    except ValueError:
                        continue
        
        return None, None
    
    def _extract_education(self, text: str) -> List[str]:
        """Extrae requisitos de formación."""
        education_keywords = [
            r'(?:grado|degree|licenciatura|bachelor)\\s+(?:en|in)\\s+([^.,;]+)',
            r'(?:máster|master|msc)\\s+(?:en|in)?\\s*([^.,;]+)',
            r'(?:doctorado|phd)\\s+(?:en|in)?\\s*([^.,;]+)',
            r'(?:formación|education)[^.,]*(?:en|in)\\s+([^.,;]+)',
        ]
        
        education = []
        for pattern in education_keywords:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend([m.strip() for m in matches if len(m.strip()) > 3])
        
        return list(set(education))
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extrae certificaciones requeridas o deseables."""
        cert_patterns = [
            r'(?:AWS|Amazon Web Services)[\\s\\w]*Certified[\\s\\w]*',
            r'(?:Microsoft|Azure)[\\s\\w]*Certified[\\s\\w]*',
            r'(?:Google|GCP)[\\s\\w]*Certified[\\s\\w]*',
            r'PMP[\\s\\w]*',
            r'(?:Scrum Master|CSM)[\\s\\w]*',
            r'ITIL[\\s\\w]*',
            r'Cisco[\\s\\w]*CCNA[\\s\\w]*',
            r'CompTIA[\\s\\w]*',
            r'(?:certificación|certification)[^.,]*(?:en|in)?\\s+([^.,;]+)',
        ]
        
        certs = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certs.extend(matches)
        
        return list(set(certs))
    
    def _extract_languages(self, text: str) -> List[Dict[str, str]]:
        """Extrae requisitos de idiomas."""
        languages = []
        
        lang_patterns = [
            r'(español|spanish)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(inglés|english)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(francés|french)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(alemán|german)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(italiano|italian)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(portugués|portuguese)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
        ]
        
        for pattern in lang_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(match)
                
                level_match = re.search(r'(nativo|native|C2|C1|B2|B1|A2|A1)', match, re.IGNORECASE)
                level = level_match.group(1) if level_match else "No especificado"
                
                lang_match = re.search(r'(español|inglés|francés|alemán|italiano|portugués|spanish|english|french|german|italian|portuguese)', match, re.IGNORECASE)
                lang = lang_match.group(1) if lang_match else "Desconocido"
                
                languages.append({"language": lang, "level": level})
        
        return languages
    
    def _extract_salary(self, text: str) -> Optional[Tuple[float, float]]:
        """Extrae rango salarial."""
        for pattern in self.SALARY_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    min_sal = float(match.group(1).replace(",", ""))
                    max_sal = float(match.group(2).replace(",", ""))
                    return (min_sal, max_sal)
                except (ValueError, AttributeError):
                    continue
        
        return None
    
    def _extract_employment_type(self, text: str) -> str:
        """Extrae tipo de empleo."""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["full-time", "tiempo completo", "jornada completa"]):
            return "full-time"
        elif any(kw in text_lower for kw in ["part-time", "tiempo parcial", "media jornada"]):
            return "part-time"
        elif any(kw in text_lower for kw in ["contract", "contrato", "freelance", "autónomo"]):
            return "contract"
        elif any(kw in text_lower for kw in ["internship", "prácticas", "becario"]):
            return "internship"
        
        return "full-time"  # Default
    
    def _extract_remote_policy(self, text: str) -> str:
        """Extrae política de trabajo remoto."""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["100% remote", "fully remote", "remoto 100%", "teletrabajo"]):
            return "remote"
        elif any(kw in text_lower for kw in ["hybrid", "híbrido", "mixto", "flexible"]):
            return "hybrid"
        elif any(kw in text_lower for kw in ["on-site", "presencial", "oficina", "office"]):
            return "on-site"
        
        return "unknown"
```

---

## 6. Explicación Línea a Línea

### JobParser

| Línea | Explicación |
|-------|-------------|
| `@dataclass` | Genera automáticamente __init__, __repr__, __eq__ |
| `field(default_factory=list)` | Evita mutable default argument antipattern |
| `re.sub(r'<[^>]+>', ' ', text)` | Elimina tags HTML con regex |
| `r'\b' + re.escape(skill) + r'\b'` | Word boundaries para match exacto |
| `sections.get("requirements", text)` | Fallback a texto completo si no hay sección |

---

## 7. Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| Skills no detectadas | Sinónimos o abreviaturas | Usar embeddings para similaridad |
| Experiencia incorrecta | Múltiples rangos | Priorizar sección de requisitos |
| Ubicación ambigua | Nombres de empresa similares | Usar NER geográfico |
| Salario no extraído | Formatos variados | Añadir más patrones + LLM |
| Soft skills mezcladas | Lenguaje vago | Usar LLM para clasificación |

---

## 8. Ejercicios

### 🟢 Nivel Básico

1. **Parsear** 5 ofertas reales de LinkedIn/Indeed y comparar resultados.
2. **Añadir** 15 skills técnicas nuevas al diccionario.
3. **Mejorar** detección de experiencia para formatos como "3-5 años".

### 🟡 Nivel Intermedio

4. **Implementar** web scraping para obtener ofertas automáticamente.
5. **Crear** sistema de sinónimos para skills ("JS" = "JavaScript").
6. **Añadir** extracción de nivel de seniority (junior/senior/lead).

### 🔴 Nivel Avanzado

7. **Usar** LLM local para extracción zero-shot de requisitos.
8. **Implementar** clasificación de ofertas por sector/industria.
9. **Crear** sistema de detección de skills emergentes (tendencias).

---

## 9. Reto Profesional

**Escenario:** Necesitas procesar 500 ofertas diarias de múltiples fuentes (LinkedIn, Indeed, InfoJobs).

**Entregable:**
- Scraper multi-fuente con rotación de proxies
- Pipeline de normalización de skills (taxonomy)
- API para consultar ofertas procesadas
- Dashboard de tendencias de mercado laboral

---

**[⬅️ Módulo 3: Procesamiento de CV](03-procesamiento-cv.md) | [➡️ Módulo 5: Matching Inteligente](05-matching.md)**
'''
