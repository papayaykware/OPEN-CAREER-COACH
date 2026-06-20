
# MÓDULO 3: Procesamiento de Currículums

> **Duración estimada:** 6-8 horas | **Nivel:** Intermedio

---

## 1. Introducción

Este módulo construye el pipeline completo de extracción de información de currículums. Aprenderás a leer PDFs, DOCX y TXT, y a extraer entidades estructuradas como formación, experiencia, habilidades y certificaciones usando NLP avanzado.

---

## 2. Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Extraer texto de PDF, DOCX y TXT
- ✅ Identificar entidades nombradas (NER) en CVs
- ✅ Clasificar secciones de un currículum
- ✅ Extraer habilidades técnicas y blandas
- ✅ Calcular años de experiencia
- ✅ Estructurar datos en formato JSON estandarizado

---

## 3. Fundamentos Teóricos

### 3.1 Formatos de Documento

| Formato | Librería Python | Ventajas | Desventajas |
|---------|----------------|----------|-------------|
| **PDF** | PyPDF2, pdfplumber | Universal, preserva formato | Tablas complejas, imágenes |
| **DOCX** | python-docx | Estructura XML accesible | Solo formato moderno |
| **TXT** | Built-in | Simple, sin formato | Sin metadatos ni estructura |
| **HTML** | BeautifulSoup | Web scraping | No estándar para CVs |

### 3.2 Named Entity Recognition (NER)

El **NER** identifica y clasifica entidades en texto:

```
"Juan trabajó como Ingeniero de Software en Google desde 2020"
     PER              ORG                    DATE
```

**Entidades relevantes para CVs:**
- **PER**: Nombres de personas
- **ORG**: Empresas, universidades
- **DATE**: Fechas de inicio/fin
- **GPE**: Ubicaciones geográficas
- **MISC**: Certificaciones, títulos

### 3.3 Extracción de Habilidades

**Hard Skills:** Técnicas, medibles, específicas de dominio
- Python, Docker, Kubernetes, AWS, React, SQL

**Soft Skills:** Interpersonales, difíciles de cuantificar
- Liderazgo, comunicación, trabajo en equipo, resolución de problemas

**Métodos de extracción:**
1. **Diccionario**: Lista predefinida de términos
2. **NER**: Identificación automática con spaCy
3. **LLM**: Extracción con prompts estructurados
4. **Embeddings**: Similitud semántica con skill taxonomy

### 3.4 Pipeline de Procesamiento

```
Documento (PDF/DOCX/TXT)
         │
         ▼
┌─────────────────┐
│  Extracción de  │───▶ Texto plano + metadatos
│  Texto          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocesamiento│───▶ Normalización, eliminación de ruido
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Segmentación   │───▶ Identificar secciones (Experiencia, Formación...)
│  de Secciones   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extracción de  │───▶ NER + NLP + LLM
│  Entidades      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Estructuración │───▶ JSON estandarizado
│  de Datos       │
└─────────────────┘
```

---

## 4. Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│              PIPELINE DE PROCESAMIENTO DE CV                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                            │
│  │   Input     │                                            │
│  │  PDF/DOCX   │                                            │
│  │   TXT       │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              EXTRACTORES DE TEXTO                   │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │    │
│  │  │  PDF    │  │  DOCX   │  │  TXT    │              │    │
│  │  │Extractor│  │Extractor│  │Extractor│              │    │
│  │  │PyPDF2   │  │python-  │  │Built-in │              │    │
│  │  │pdfplum. │  │docx     │  │         │              │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘              │    │
│  │       └─────────────┴─────────────┘                 │    │
│  │                    │                                │    │
│  │                    ▼                                │    │
│  │           Texto Plano + Metadatos                   │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           PREPROCESAMIENTO                          │    │
│  │  • Normalización Unicode                            │    │
│  │  • Eliminación de caracteres especiales             │    │
│  │  • Corrección de espacios                           │    │
│  │  • Detección de idioma                              │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         SEGMENTACIÓN DE SECCIONES                   │    │
│  │                                                     │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │    │
│  │  │Personal │ │Experienc.│ │Formación │ │Skills │    │    │
│  │  │Info     │ │Laboral   │ │Académica │ │& Certs│    │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │    │
│  │                                                     │    │
│  │  Métodos: Regex + Keywords + ML Classifier          │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         EXTRACCIÓN DE ENTIDADES                     │    │
│  │                                                     │    │
│  │  ┌─────────────┐    ┌─────────────┐                 │    │
│  │  │   spaCy     │    │ Transformers│                 │    │
│  │  │   NER       │    │   (LLM)     │                 │    │
│  │  │             │    │             │                 │    │
│  │  │ • Personas  │    │ • Skills    │                 │    │
│  │  │ • Empresas  │    │ • Títulos   │                 │    │
│  │  │ • Fechas    │    │ • Resumen   │                 │    │
│  │  │ • Lugares   │    │ • Inferencia│                 │    │
│  │  └─────────────┘    └─────────────┘                 │    │
│  │                                                     │    │
│  │  ┌─────────────┐                                    │    │
│  │  │  Diccionario│───▶ Skills técnicas predefinidas  │    │
│  │  │  de Skills  │                                    │    │
│  │  └─────────────┘                                    │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         ESTRUCTURACIÓN JSON                         │    │
│  │                                                     │    │
│  │  {                                                  │    │
│  │    "personal_info": {...},                          │    │
│  │    "experience": [...],                             │    │
│  │    "education": [...],                              │    │
│  │    "skills": {                                      │    │
│  │      "technical": [...],                            │    │
│  │      "soft": [...]                                  │    │
│  │    },                                               │    │
│  │    "certifications": [...],                         │    │
│  │    "languages": [...],                              │    │
│  │    "total_experience_years": 5.5                    │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Implementación (Código)

### 5.1 Extractores de Texto

```python
# src/cv_parser/pdf_extractor.py
"""Extractor de texto para archivos PDF."""

import io
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class PDFExtractor:
    """Extrae texto de archivos PDF usando múltiples estrategias."""
    
    def __init__(self, use_pdfplumber: bool = True):
        self.use_pdfplumber = use_pdfplumber and PDFPLUMBER_AVAILABLE
        if not self.use_pdfplumber and not PYPDF2_AVAILABLE:
            raise ImportError("Instalar pdfplumber o PyPDF2")
    
    def extract(self, file_path: str) -> dict:
        """Extrae texto y metadatos de un PDF.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Dict con 'text', 'pages', 'metadata'
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        if self.use_pdfplumber:
            return self._extract_with_pdfplumber(file_path)
        return self._extract_with_pypdf2(file_path)
    
    def _extract_with_pdfplumber(self, file_path: str) -> dict:
        """Extracción con pdfplumber (mejor para tablas)."""
        text_parts = []
        metadata = {}
        
        with pdfplumber.open(file_path) as pdf:
            metadata = {
                "total_pages": len(pdf.pages),
                "file_name": Path(file_path).name,
            }
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return {
            "text": "\\n\\n".join(text_parts),
            "pages": len(text_parts),
            "metadata": metadata,
            "extractor": "pdfplumber",
        }
    
    def _extract_with_pypdf2(self, file_path: str) -> dict:
        """Extracción con PyPDF2 (fallback)."""
        text_parts = []
        
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            metadata = {
                "total_pages": len(reader.pages),
                "file_name": Path(file_path).name,
            }
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        
        return {
            "text": "\\n\\n".join(text_parts),
            "pages": len(text_parts),
            "metadata": metadata,
            "extractor": "PyPDF2",
        }
```

```python
# src/cv_parser/docx_extractor.py
"""Extractor de texto para archivos DOCX."""

from pathlib import Path
from typing import Dict

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class DOCXExtractor:
    """Extrae texto de archivos Microsoft Word."""
    
    def __init__(self):
        if not DOCX_AVAILABLE:
            raise ImportError("Instalar: pip install python-docx")
    
    def extract(self, file_path: str) -> Dict:
        """Extrae texto y metadatos de un DOCX."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        doc = Document(file_path)
        
        # Extraer texto de párrafos
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        # Extraer texto de tablas
        table_texts = []
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells)
                if row_text.strip():
                    table_texts.append(row_text)
        
        # Metadatos
        metadata = {
            "file_name": path.name,
            "paragraphs": len(paragraphs),
            "tables": len(doc.tables),
        }
        
        # Intentar extraer propiedades del documento
        try:
            core_props = doc.core_properties
            metadata.update({
                "author": core_props.author,
                "created": str(core_props.created) if core_props.created else None,
                "modified": str(core_props.modified) if core_props.modified else None,
            })
        except Exception:
            pass
        
        all_text = "\\n\\n".join(paragraphs + table_texts)
        
        return {
            "text": all_text,
            "pages": len(paragraphs) // 40 + 1,  # Estimación aproximada
            "metadata": metadata,
            "extractor": "python-docx",
        }
```

```python
# src/cv_parser/txt_extractor.py
"""Extractor de texto para archivos planos."""

from pathlib import Path
from typing import Dict


class TXTExtractor:
    """Extrae texto de archivos TXT."""
    
    def extract(self, file_path: str) -> Dict:
        """Extrae texto de un archivo TXT."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Intentar detectar encoding alternativo
        if not text.strip():
            for encoding in ["latin-1", "iso-8859-1", "cp1252"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        text = f.read()
                    if text.strip():
                        break
                except Exception:
                    continue
        
        lines = text.splitlines()
        
        return {
            "text": text,
            "pages": len(lines) // 50 + 1,
            "metadata": {
                "file_name": path.name,
                "lines": len(lines),
                "characters": len(text),
            },
            "extractor": "built-in",
        }
```

### 5.2 Extractor de Entidades

```python
# src/cv_parser/entity_extractor.py
"""Extracción de entidades de currículums usando NLP."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

import spacy
from spacy.tokens import Doc


@dataclass
class PersonalInfo:
    """Información personal extraída."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


@dataclass
class ExperienceEntry:
    """Entrada de experiencia laboral."""
    company: str = ""
    title: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str = ""
    location: Optional[str] = None
    is_current: bool = False


@dataclass
class EducationEntry:
    """Entrada de formación académica."""
    institution: str = ""
    degree: str = ""
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[float] = None


@dataclass
class CVData:
    """Datos estructurados de un currículum."""
    personal_info: PersonalInfo = field(default_factory=PersonalInfo)
    experience: List[ExperienceEntry] = field(default_factory=list)
    education: List[EducationEntry] = field(default_factory=list)
    skills: Dict[str, List[str]] = field(default_factory=lambda: {"technical": [], "soft": []})
    certifications: List[str] = field(default_factory=list)
    languages: List[Dict[str, str]] = field(default_factory=list)
    summary: Optional[str] = None
    total_experience_years: float = 0.0
    raw_text: str = ""


class EntityExtractor:
    """Extrae entidades estructuradas de texto de CV."""
    
    # Diccionario de skills técnicas
    TECHNICAL_SKILLS = {
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "docker", "kubernetes", "aws", "azure", "gcp", "terraform",
        "react", "vue", "angular", "nodejs", "django", "flask", "fastapi",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "git", "jenkins", "gitlab-ci", "github-actions", "ansible",
        "linux", "bash", "powershell", "nginx", "apache",
        "machine learning", "deep learning", "nlp", "computer vision",
        "data science", "big data", "spark", "hadoop", "kafka",
        "rest api", "graphql", "microservices", "ci/cd", "agile", "scrum",
    }
    
    # Diccionario de soft skills
    SOFT_SKILLS = {
        "liderazgo", "leadership", "comunicación", "communication",
        "trabajo en equipo", "teamwork", "resolución de problemas",
        "problem solving", "pensamiento crítico", "critical thinking",
        "adaptabilidad", "adaptability", "creatividad", "creativity",
        "gestión del tiempo", "time management", "empatía", "empathy",
        "negociación", "negotiation", "presentación", "presentation",
    }
    
    # Patrones regex
    EMAIL_PATTERN = re.compile(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')
    PHONE_PATTERN = re.compile(r'(?:\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{2,4}\\)?[-.\\s]?\\d{2,4}[-.\\s]?\\d{2,4}')
    LINKEDIN_PATTERN = re.compile(r'linkedin\\.com/in/[\\w-]+')
    URL_PATTERN = re.compile(r'https?://(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b[-a-zA-Z0-9()@:%_\\+.~#?&/=]*')
    
    def __init__(self, model_name: str = "es_core_news_md"):
        """Inicializa el extractor con modelo spaCy.
        
        Args:
            model_name: Modelo spaCy a usar (es_core_news_md o en_core_web_md)
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Modelo {model_name} no encontrado. Descargando...")
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)
        
        # Añadir sentencizer si no existe
        if "sentencizer" not in self.nlp.pipe_names:
            self.nlp.add_pipe("sentencizer")
    
    def extract(self, text: str) -> CVData:
        """Extrae todas las entidades del texto del CV.
        
        Args:
            text: Texto completo del currículum
            
        Returns:
            CVData con toda la información estructurada
        """
        cv_data = CVData(raw_text=text)
        doc = self.nlp(text)
        
        # Extraer información personal
        cv_data.personal_info = self._extract_personal_info(text, doc)
        
        # Extraer experiencia
        cv_data.experience = self._extract_experience(text, doc)
        
        # Extraer formación
        cv_data.education = self._extract_education(text, doc)
        
        # Extraer skills
        cv_data.skills = self._extract_skills(text)
        
        # Extraer certificaciones
        cv_data.certifications = self._extract_certifications(text)
        
        # Extraer idiomas
        cv_data.languages = self._extract_languages(text)
        
        # Calcular experiencia total
        cv_data.total_experience_years = self._calculate_total_experience(cv_data.experience)
        
        return cv_data
    
    def _extract_personal_info(self, text: str, doc: Doc) -> PersonalInfo:
        """Extrae información personal."""
        info = PersonalInfo()
        
        # Email
        email_match = self.EMAIL_PATTERN.search(text)
        if email_match:
            info.email = email_match.group()
        
        # Teléfono
        phone_match = self.PHONE_PATTERN.search(text)
        if phone_match:
            info.phone = phone_match.group()
        
        # LinkedIn
        linkedin_match = self.LINKEDIN_PATTERN.search(text)
        if linkedin_match:
            info.linkedin = linkedin_match.group()
        
        # Nombre (primera PERSON encontrada en las primeras líneas)
        lines = text.split("\\n")[:10]  # Primeras 10 líneas
        header_text = " ".join(lines)
        header_doc = self.nlp(header_text)
        
        for ent in header_doc.ents:
            if ent.label_ == "PER":
                info.name = ent.text
                break
        
        # Ubicación
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC"):
                info.location = ent.text
                break
        
        return info
    
    def _extract_experience(self, text: str, doc: Doc) -> List[ExperienceEntry]:
        """Extrae experiencia laboral."""
        experiences = []
        
        # Buscar sección de experiencia
        experience_section = self._extract_section(text, [
            "experiencia", "experience", "experiencia laboral",
            "work experience", "employment history", "historial laboral"
        ])
        
        if not experience_section:
            return experiences
        
        # Dividir en entradas (por líneas en blanco o fechas)
        entries = re.split(r'\\n\\s*\\n', experience_section)
        
        for entry_text in entries:
            if len(entry_text.strip()) < 20:
                continue
            
            exp = ExperienceEntry()
            
            # Extraer fechas
            dates = self._extract_dates(entry_text)
            if dates:
                exp.start_date = dates[0]
                if len(dates) > 1:
                    exp.end_date = dates[1]
                    exp.is_current = "present" in entry_text.lower() or "actual" in entry_text.lower()
            
            # Extraer empresa (ORG)
            entry_doc = self.nlp(entry_text[:500])  # Limitar para rendimiento
            for ent in entry_doc.ents:
                if ent.label_ == "ORG":
                    exp.company = ent.text
                    break
            
            # Extraer título (línea que contiene palabras clave)
            lines = entry_text.split("\\n")
            for line in lines[:3]:
                line_lower = line.lower()
                if any(kw in line_lower for kw in ["ingeniero", "developer", "manager", "analista", "consultor", "arquitecto", "lead", "senior", "junior"]):
                    exp.title = line.strip()
                    break
            
            exp.description = entry_text
            experiences.append(exp)
        
        return experiences
    
    def _extract_education(self, text: str, doc: Doc) -> List[EducationEntry]:
        """Extrae formación académica."""
        educations = []
        
        education_section = self._extract_section(text, [
            "educación", "education", "formación", "formacion",
            "academic", "estudios", "titulación", "titulacion"
        ])
        
        if not education_section:
            return educations
        
        entries = re.split(r'\\n\\s*\\n', education_section)
        
        for entry_text in entries:
            if len(entry_text.strip()) < 15:
                continue
            
            edu = EducationEntry()
            
            # Extraer fechas
            dates = self._extract_dates(entry_text)
            if dates:
                edu.start_date = dates[0]
                if len(dates) > 1:
                    edu.end_date = dates[1]
            
            # Extraer institución (ORG)
            entry_doc = self.nlp(entry_text[:300])
            for ent in entry_doc.ents:
                if ent.label_ == "ORG":
                    edu.institution = ent.text
                    break
            
            # Detectar grado
            lines = entry_text.split("\\n")
            for line in lines[:3]:
                line_lower = line.lower()
                if any(kw in line_lower for kw in ["grado", "master", "máster", "doctorado", "phd", "licenciatura", "ingeniería", "bachiller"]):
                    edu.degree = line.strip()
                    break
            
            educations.append(edu)
        
        return educations
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extrae habilidades técnicas y blandas."""
        text_lower = text.lower()
        
        technical = []
        soft = []
        
        # Skills técnicas
        for skill in self.TECHNICAL_SKILLS:
            # Buscar palabra completa
            pattern = r'\\b' + re.escape(skill) + r'\\b'
            if re.search(pattern, text_lower):
                technical.append(skill)
        
        # Soft skills
        for skill in self.SOFT_SKILLS:
            pattern = r'\\b' + re.escape(skill) + r'\\b'
            if re.search(pattern, text_lower):
                soft.append(skill)
        
        return {
            "technical": list(set(technical)),
            "soft": list(set(soft)),
        }
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extrae certificaciones."""
        certs = []
        
        # Patrones comunes de certificación
        cert_patterns = [
            r'(?:AWS|Amazon Web Services)[\\s\\w]*Certified[\\s\\w]*',
            r'(?:Microsoft|Azure)[\\s\\w]*Certified[\\s\\w]*',
            r'(?:Google|GCP)[\\s\\w]*Certified[\\s\\w]*',
            r'PMP[\\s\\w]*',
            r'Scrum Master[\\s\\w]*',
            r'ITIL[\\s\\w]*',
            r'Cisco[\\s\\w]*CCNA[\\s\\w]*',
            r'CompTIA[\\s\\w]*',
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certs.extend(matches)
        
        # Buscar en sección de certificaciones
        cert_section = self._extract_section(text, [
            "certificaciones", "certifications", "certificados", "certs"
        ])
        
        if cert_section:
            lines = [l.strip() for l in cert_section.split("\\n") if l.strip() and len(l.strip()) > 5]
            certs.extend(lines[:10])  # Limitar
        
        return list(set(certs))
    
    def _extract_languages(self, text: str) -> List[Dict[str, str]]:
        """Extrae idiomas y niveles."""
        languages = []
        
        # Patrones de idioma + nivel
        lang_patterns = [
            r'(español|spanish)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(inglés|english)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(francés|french)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
            r'(alemán|german)[\\s\\w]*(?:nativo|native|C2|C1|B2|B1|A2|A1)',
        ]
        
        for pattern in lang_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(match)
                
                # Extraer nivel
                level_match = re.search(r'(nativo|native|C2|C1|B2|B1|A2|A1)', match, re.IGNORECASE)
                level = level_match.group(1) if level_match else "No especificado"
                
                # Extraer idioma
                lang_match = re.search(r'(español|inglés|francés|alemán|spanish|english|french|german)', match, re.IGNORECASE)
                lang = lang_match.group(1) if lang_match else "Desconocido"
                
                languages.append({
                    "language": lang,
                    "level": level,
                })
        
        return languages
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extrae fechas del texto."""
        date_patterns = [
            r'\\b(19|20)\\d{2}\\b',  # Años 1900-2099
            r'\\b\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}\\b',
            r'\\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\\s+\\d{4}\\b',
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return dates[:4]  # Limitar
    
    def _extract_section(self, text: str, headers: List[str]) -> Optional[str]:
        """Extrae una sección del CV basada en encabezados."""
        lines = text.split("\\n")
        section_start = -1
        section_end = len(lines)
        
        # Encontrar inicio de sección
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            # Eliminar caracteres especiales para comparación
            line_clean = re.sub(r'[^\\w\\s]', '', line_lower)
            
            for header in headers:
                header_clean = re.sub(r'[^\\w\\s]', '', header.lower())
                if header_clean in line_clean or line_clean in header_clean:
                    section_start = i + 1
                    break
            if section_start >= 0:
                break
        
        if section_start < 0:
            return None
        
        # Encontrar fin de sección (próximo encabezado en mayúsculas o con formato)
        for i in range(section_start, min(section_start + 50, len(lines))):
            line = lines[i].strip()
            # Detectar próximo encabezado (línea corta, mayúsculas, o con separadores)
            if len(line) > 0 and len(line) < 40:
                if line.isupper() or line.endswith(":") or re.match(r'^[-=]{3,}$', line):
                    section_end = i
                    break
        
        section_text = "\\n".join(lines[section_start:section_end])
        return section_text.strip()
    
    def _calculate_total_experience(self, experiences: List[ExperienceEntry]) -> float:
        """Calcula años totales de experiencia."""
        total_months = 0
        
        for exp in experiences:
            if not exp.start_date:
                continue
            
            try:
                # Extraer año de inicio
                start_year = int(re.search(r'(19|20)\\d{2}', str(exp.start_date)).group())
                
                if exp.is_current or not exp.end_date:
                    end_year = datetime.now().year
                else:
                    end_match = re.search(r'(19|20)\\d{2}', str(exp.end_date))
                    end_year = int(end_match.group()) if end_match else datetime.now().year
                
                total_months += (end_year - start_year) * 12
            except (AttributeError, ValueError):
                continue
        
        return round(total_months / 12, 1)
```

### 5.3 Pipeline Principal

```python
# src/cv_parser/cv_pipeline.py
"""Pipeline completo de procesamiento de currículums."""

from pathlib import Path
from typing import Union

from .pdf_extractor import PDFExtractor
from .docx_extractor import DOCXExtractor
from .txt_extractor import TXTExtractor
from .entity_extractor import EntityExtractor, CVData


class CVPipeline:
    """Pipeline unificado para procesar currículums en cualquier formato."""
    
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.docx_extractor = DOCXExtractor()
        self.txt_extractor = TXTExtractor()
        self.entity_extractor = EntityExtractor()
    
    def process(self, file_path: Union[str, Path]) -> CVData:
        """Procesa un currículum y devuelve datos estructurados.
        
        Args:
            file_path: Ruta al archivo del CV
            
        Returns:
            CVData con toda la información extraída
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Extraer texto según formato
        suffix = path.suffix.lower()
        
        if suffix == ".pdf":
            extraction = self.pdf_extractor.extract(str(path))
        elif suffix == ".docx":
            extraction = self.docx_extractor.extract(str(path))
        elif suffix == ".txt":
            extraction = self.txt_extractor.extract(str(path))
        else:
            raise ValueError(f"Formato no soportado: {suffix}")
        
        # Extraer entidades
        cv_data = self.entity_extractor.extract(extraction["text"])
        
        # Añadir metadatos de extracción
        cv_data.metadata = {
            "file_name": path.name,
            "file_format": suffix,
            "extraction_method": extraction.get("extractor", "unknown"),
            "pages": extraction.get("pages", 0),
        }
        
        return cv_data
    
    def process_text(self, text: str) -> CVData:
        """Procesa texto directamente (útil para testing)."""
        return self.entity_extractor.extract(text)
```

---

## 6. Explicación Línea a Línea

### PDFExtractor

| Línea | Explicación |
|-------|-------------|
| `pdfplumber.open(file_path) as pdf` | Context manager que abre y cierra el PDF automáticamente |
| `page.extract_text()` | Extrae texto manteniendo layout, ideal para tablas |
| `PyPDF2.PdfReader(f)` | Clase moderna de PyPDF2 (reemplaza PdfFileReader) |
| `"\\n\\n".join(text_parts)` | Une páginas con doble salto para separación visual |

### EntityExtractor

| Línea | Explicación |
|-------|-------------|
| `spacy.load(model_name)` | Carga modelo preentrenado de spaCy |
| `re.search(pattern, text_lower)` | Búsqueda case-insensitive de skills |
| `r'\\b' + re.escape(skill) + r'\\b'` | Word boundaries para coincidencia exacta |
| `self.nlp(header_text)` | Procesa solo las primeras líneas para rendimiento |
| `datetime.now().year` | Calcula año actual para experiencia en curso |

---

## 7. Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| PDF escaneado (imagen) | Sin texto extraíble | Usar OCR con pytesseract |
| Tablas mal formateadas | Layout complejo | Usar pdfplumber en lugar de PyPDF2 |
| Fechas incorrectas | Formatos variados | Añadir más patrones regex |
| Skills no detectadas | Sinónimos o abreviaturas | Expandir diccionario + embeddings |
| Nombre no encontrado | Formato inusual | Añadir heurísticas de posición |
| Secciones mal divididas | Encabezados inconsistentes | ML classifier para secciones |

---

## 8. Ejercicios

### 🟢 Nivel Básico

1. **Procesar** 3 CVs de ejemplo y comparar resultados manualmente.
2. **Añadir** 10 skills técnicas nuevas al diccionario.
3. **Mejorar** el extractor de teléfonos para soportar formatos internacionales.

### 🟡 Nivel Intermedio

4. **Implementar** OCR para PDFs escaneados usando pytesseract.
5. **Crear** un clasificador ML para detectar secciones de CV.
6. **Añadir** soporte para extracción de proyectos personales/GitHub.

### 🔴 Nivel Avanzado

7. **Usar** un LLM local (Ollama) para extracción zero-shot de entidades.
8. **Implementar** resolución de coreferencia para enlazar pronombres con entidades.
9. **Crear** un sistema de validación automática contra ground truth.

---

## 9. Reto Profesional

**Escenario:** Tu startup recibe 1,000 CVs diarios en múltiples formatos y idiomas. Necesitas un pipeline de producción.

**Entregable:**
- Pipeline con cola de procesamiento (Celery/RQ)
- Sistema de OCR para PDFs escaneados
- Validación de calidad con métricas (precision/recall)
- API REST para procesamiento asíncrono
- Dashboard de métricas de extracción

---

## 📚 Recursos Adicionales

- [spaCy Documentation](https://spacy.io/usage)
- [PyPDF2 GitHub](https://github.com/py-pdf/pypdf)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

**[⬅️ Módulo 2: Entorno](02-entorno.md) | [➡️ Módulo 4: Procesamiento de Ofertas](04-procesamiento-ofertas.md)**
'''

