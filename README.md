> ★ Nuevo en v1.1.0

---

# ⚙️ Instalación

```bash
git clone https://github.com/papayaykware/OPEN-CAREER-COACH
cd OPEN-CAREER-COACH
pip install -r requirements.txt
```

La primera ejecución de la interfaz Gradio descarga el modelo de embeddings (~80 MB desde Hugging Face). Requiere conexión a internet ese primer arranque.

---

# ▶️ Uso Rápido

### Opción A — CLI simple (sin modelo de embeddings)

```bash
python run_mvp.py
```

Solicita habilidades y requisitos por teclado (separados por comas) y devuelve un score básico de coincidencia. Útil para pruebas rápidas sin dependencias pesadas.

### Opción B — Interfaz Gradio completa (recomendado)

```bash
python -m src.ui.gradio_app
```

Abre una interfaz web local. Pega el CV y la oferta en los cuadros de texto y pulsa **Analizar matching** para obtener:

- Score global con nivel de encaje visual
- Desglose por 5 dimensiones semánticas
- Gap analysis requisito a requisito
- Skills coincidentes, faltantes y recomendaciones
- Descarga del informe en Markdown y JSON

### Ejecutar los tests

```bash
pytest tests/test_explainer.py -v
```

---

# 🔍 Matching Explicable

El `MatchingExplainer` analiza CV y oferta en 5 dimensiones con pesos por defecto configurables:

| Dimensión | Peso por defecto |
|-----------|-----------------|
| Habilidades técnicas | 35% |
| Experiencia | 25% |
| Formación | 15% |
| Habilidades blandas | 15% |
| Idiomas | 10% |

Uso programático:

```python
from src.matching.explainer import MatchingExplainer

explainer = MatchingExplainer()
result = explainer.explain(cv_text, offer_text)

print(result.global_score)     # 0.0 – 1.0
print(result.narrative)        # texto explicativo
print(result.gap_analysis)     # lista de RequirementMatch
print(result.dimension_scores) # lista de DimensionScore
```

Los pesos son inyectables para adaptar el análisis a perfiles de puesto específicos:

```python
explainer = MatchingExplainer(dimension_weights={
    "habilidades_tecnicas": 0.50,
    "experiencia":          0.30,
    "formacion":            0.10,
    "habilidades_blandas":  0.05,
    "idiomas":              0.05,
})
```

---

# 📥 Exportación de Informes

```python
from src.matching.explainer import MatchingExplainer
from src.exporter.report_exporter import ReportExporter

explainer = MatchingExplainer()
exporter  = ReportExporter()          # guarda en reports/ por defecto

result = explainer.explain(cv_text, offer_text)
rutas  = exporter.export(result, nombre_base="mi_informe")

print(rutas["md"])    # reports/mi_informe_20260626_143022.md
print(rutas["json"])  # reports/mi_informe_20260626_143022.json
```

Para generar solo un formato:

```python
rutas = exporter.export(result, formatos=["json"])
```

---

# 🔁 Ejemplo de Flujo Completo

```python
from src.cv_parser.cv_pipeline import CVPipeline
from src.job_parser.job_pipeline import JobPipeline
from src.matching.similarity import CVJobMatcher
from src.matching.explainer import MatchingExplainer
from src.exporter.report_exporter import ReportExporter

# Parsing
cv_data  = CVPipeline().process_text(cv_text)   # o .process("cv.pdf")
job_data = JobPipeline().process(offer_text)

# Matching base
matcher  = CVJobMatcher()
base     = matcher.calculate_match(cv_data.__dict__, job_data.__dict__)

# Matching explicable
explainer = MatchingExplainer()
explained = explainer.explain(cv_text, offer_text)

print("Score base:", base.global_score)
print("Score explicable:", explained.global_score)
print(explained.narrative)

# Exportación
exporter = ReportExporter()
rutas = exporter.export(explained, base, nombre_base="informe")
print("Informe MD:", rutas["md"])
print("Informe JSON:", rutas["json"])
```

---

# 🗺️ Roadmap

### ✅ v1.0.0 — MVP funcional (junio 2026)
- Pipeline CV + oferta + matching semántico
- Interfaz Gradio mínima

### ✅ v1.0.1 — Corrección de errores (junio 2026)
- 4 bugs críticos resueltos (ver CHANGELOG)

### 🔄 v1.1.0 — Matching explicable (en desarrollo)
- `MatchingExplainer`: análisis dimensional + gap analysis + narrativa
- UI Gradio renovada con tabs y exportación integrada
- `ReportExporter`: informes MD y JSON
- Suite de tests pytest

### 🔮 v2.0.0 — Producto completo (futuro)
- API REST con FastAPI
- UI profesional (React / Streamlit)
- Base de datos para histórico de análisis
- Dashboard de métricas
- Sistema de autenticación opcional

---

# ✍️ Autoría

Este proyecto es desarrollado bajo un modelo de **co-autoría estructurada**:

- **Director y originador:** Javi Ciborro ([@papayaykware](https://github.com/papayaykware))
- **Autor conceptual:** Claude (Anthropic)

---

# 🤝 Contribuir

Las contribuciones son bienvenidas. Puedes abrir un **issue**, enviar un **pull request** o proponer mejoras en las [discusiones](https://github.com/papayaykware/OPEN-CAREER-COACH/issues).

---

# 📄 Licencia

Este proyecto está bajo licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
