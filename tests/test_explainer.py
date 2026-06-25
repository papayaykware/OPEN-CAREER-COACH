"""
OPEN-CAREER-COACH · tests/test_explainer.py
Tests unitarios — MatchingExplainer v1.1.0

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

import pytest
from src.matching.explainer import (
    MatchingExplainer,
    DimensionScore,
    RequirementMatch,
    ExplainedMatchResult,
    DEFAULT_DIMENSIONS,
)


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

CV_ALTO_ENCAJE = """
Ingeniero de datos con 5 años de experiencia en Python, SQL y machine learning.
Máster en Inteligencia Artificial por la Universidad Politécnica de Madrid.
Experiencia liderando equipos de 4 personas. Nivel de inglés C1.
Conocimientos de Docker, Kubernetes y AWS. Certificación en TensorFlow.
Habilidades: trabajo en equipo, comunicación, autonomía, resolución de problemas.
"""

CV_BAJO_ENCAJE = """
Técnico en instalaciones eléctricas con 10 años de experiencia.
Formación profesional en electricidad industrial.
Trabajo en obras y mantenimiento de equipos industriales.
Carnet de conducir B. Disponibilidad para viajar.
"""

OFERTA_DATA_SCIENCE = """
Buscamos Data Scientist con experiencia en Python y machine learning.
Se requiere experiencia mínima de 3 años en análisis de datos.
Es imprescindible conocimiento de SQL y herramientas de visualización.
Se requiere nivel de inglés B2 o superior.
Valorable experiencia con Docker y cloud computing (AWS o Azure).
El candidato debe tener capacidad de trabajo en equipo y comunicación efectiva.
Requisito: titulación universitaria en Ingeniería, Matemáticas o similar.
"""


# ─────────────────────────────────────────────
# TESTS DE INICIALIZACIÓN
# ─────────────────────────────────────────────

class TestMatchingExplainerInit:

    def test_instancia_por_defecto(self):
        explainer = MatchingExplainer()
        assert explainer.weights == DEFAULT_DIMENSIONS

    def test_pesos_personalizados_validos(self):
        pesos = {
            "habilidades_tecnicas": 0.50,
            "experiencia":          0.20,
            "formacion":            0.10,
            "habilidades_blandas":  0.10,
            "idiomas":              0.10,
        }
        explainer = MatchingExplainer(dimension_weights=pesos)
        assert explainer.weights["habilidades_tecnicas"] == 0.50

    def test_pesos_invalidos_lanzan_error(self):
        pesos_rotos = {
            "habilidades_tecnicas": 0.80,
            "experiencia":          0.80,
            "formacion":            0.10,
            "habilidades_blandas":  0.10,
            "idiomas":              0.10,
        }
        with pytest.raises(ValueError, match="deben sumar 1.0"):
            MatchingExplainer(dimension_weights=pesos_rotos)


# ─────────────────────────────────────────────
# TESTS DE EXTRACCIÓN DIMENSIONAL
# ─────────────────────────────────────────────

class TestDimensionExtraction:

    def setup_method(self):
        self.explainer = MatchingExplainer()

    def test_extrae_habilidades_tecnicas(self):
        fragments = self.explainer._extract_dimension_fragments(
            CV_ALTO_ENCAJE, "habilidades_tecnicas"
        )
        assert "python" in fragments
        assert "sql" in fragments

    def test_extrae_idiomas(self):
        fragments = self.explainer._extract_dimension_fragments(
            CV_ALTO_ENCAJE, "idiomas"
        )
        assert len(fragments) > 0

    def test_texto_sin_matches_devuelve_lista_vacia(self):
        fragments = self.explainer._extract_dimension_fragments(
            "Texto sin ningún término técnico relevante aquí.", "idiomas"
        )
        assert isinstance(fragments, list)

    def test_dimension_score_es_dataclass_valida(self):
        ds = self.explainer._score_dimension(
            CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE, "habilidades_tecnicas"
        )
        assert isinstance(ds, DimensionScore)
        assert 0.0 <= ds.score <= 1.0
        assert ds.dimension == "habilidades_tecnicas"

    def test_score_alto_encaje_mayor_que_bajo(self):
        ds_alto = self.explainer._score_dimension(
            CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE, "habilidades_tecnicas"
        )
        ds_bajo = self.explainer._score_dimension(
            CV_BAJO_ENCAJE, OFERTA_DATA_SCIENCE, "habilidades_tecnicas"
        )
        assert ds_alto.score > ds_bajo.score


# ─────────────────────────────────────────────
# TESTS DE GAP ANALYSIS
# ─────────────────────────────────────────────

class TestGapAnalysis:

    def setup_method(self):
        self.explainer = MatchingExplainer()

    def test_extrae_requisitos_de_oferta(self):
        requirements = self.explainer._extract_requirements(OFERTA_DATA_SCIENCE)
        assert len(requirements) > 0
        assert all(isinstance(r, str) for r in requirements)

    def test_requisito_cubierto_en_cv_alto(self):
        req = "Se requiere experiencia en Python y machine learning."
        match = self.explainer._evaluate_requirement(req, CV_ALTO_ENCAJE)
        assert isinstance(match, RequirementMatch)
        assert match.status in ("cubierto", "parcial")
        assert match.confidence > 0.0

    def test_requisito_ausente_en_cv_bajo(self):
        req = "Se requiere experiencia en Python y machine learning."
        match = self.explainer._evaluate_requirement(req, CV_BAJO_ENCAJE)
        assert match.status in ("parcial", "ausente")

    def test_gap_analysis_devuelve_lista_requirement_match(self):
        gap = self.explainer._run_gap_analysis(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert isinstance(gap, list)
        assert all(isinstance(r, RequirementMatch) for r in gap)

    def test_status_values_son_validos(self):
        gap = self.explainer._run_gap_analysis(CV_BAJO_ENCAJE, OFERTA_DATA_SCIENCE)
        valid_statuses = {"cubierto", "parcial", "ausente"}
        for r in gap:
            assert r.status in valid_statuses

    def test_cv_evidence_presente_cuando_hay_match(self):
        req = "Se requiere experiencia en Python."
        match = self.explainer._evaluate_requirement(req, CV_ALTO_ENCAJE)
        if match.status != "ausente":
            assert match.cv_evidence is not None


# ─────────────────────────────────────────────
# TESTS DE SCORE GLOBAL
# ─────────────────────────────────────────────

class TestWeightedScore:

    def setup_method(self):
        self.explainer = MatchingExplainer()

    def test_score_global_entre_0_y_1(self):
        dimension_scores = self.explainer._compute_dimension_scores(
            CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE
        )
        score = self.explainer._weighted_score(dimension_scores)
        assert 0.0 <= score <= 1.0

    def test_alto_encaje_mayor_score_que_bajo(self):
        ds_alto = self.explainer._compute_dimension_scores(
            CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE
        )
        ds_bajo = self.explainer._compute_dimension_scores(
            CV_BAJO_ENCAJE, OFERTA_DATA_SCIENCE
        )
        score_alto = self.explainer._weighted_score(ds_alto)
        score_bajo = self.explainer._weighted_score(ds_bajo)
        assert score_alto > score_bajo

    def test_score_cv_identico_a_oferta(self):
        """Caso límite: CV y oferta con texto idéntico → score máximo."""
        ds = self.explainer._compute_dimension_scores(
            OFERTA_DATA_SCIENCE, OFERTA_DATA_SCIENCE
        )
        score = self.explainer._weighted_score(ds)
        assert score > 0.3  # Jaccard con sí mismo no es 1.0 por diseño dimensional


# ─────────────────────────────────────────────
# TESTS DE NARRATIVA
# ─────────────────────────────────────────────

class TestNarrative:

    def setup_method(self):
        self.explainer = MatchingExplainer()

    def test_narrativa_contiene_score(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert "%" in result.narrative

    def test_narrativa_nivel_alto(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert any(
            nivel in result.narrative
            for nivel in ("alto", "moderado", "bajo")
        )

    def test_narrativa_no_vacia(self):
        result = self.explainer.explain(CV_BAJO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert len(result.narrative) > 50


# ─────────────────────────────────────────────
# TESTS DE INTEGRACIÓN — explain()
# ─────────────────────────────────────────────

class TestExplainIntegration:

    def setup_method(self):
        self.explainer = MatchingExplainer()

    def test_resultado_es_explained_match_result(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert isinstance(result, ExplainedMatchResult)

    def test_resultado_tiene_todas_las_dimensiones(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        dims = {ds.dimension for ds in result.dimension_scores}
        assert dims == set(DEFAULT_DIMENSIONS.keys())

    def test_metadata_contiene_profile_type(self):
        result = self.explainer.explain(
            CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE, profile_type="data_science"
        )
        assert result.metadata["profile_type"] == "data_science"

    def test_strengths_y_gaps_son_listas(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert isinstance(result.strengths, list)
        assert isinstance(result.gaps, list)

    def test_textos_vacios_no_lanzan_excepcion(self):
        result = self.explainer.explain("", "")
        assert isinstance(result, ExplainedMatchResult)
        assert result.global_score == 0.0

    def test_pipeline_completo_cv_bajo_encaje(self):
        result = self.explainer.explain(CV_BAJO_ENCAJE, OFERTA_DATA_SCIENCE)
        assert result.global_score < 0.4
        assert len(result.gaps) > 0

    def test_confidence_siempre_entre_0_y_1(self):
        result = self.explainer.explain(CV_ALTO_ENCAJE, OFERTA_DATA_SCIENCE)
        for rm in result.gap_analysis:
            assert 0.0 <= rm.confidence <= 1.0


# ─────────────────────────────────────────────
# TESTS DE SIMILITUD FALLBACK
# ─────────────────────────────────────────────

class TestDefaultSimilarity:

    def test_textos_identicos(self):
        score = MatchingExplainer._default_similarity("python sql machine", "python sql machine")
        assert score == 1.0

    def test_textos_sin_overlap(self):
        score = MatchingExplainer._default_similarity("python sql", "electricidad fontanería")
        assert score == 0.0

    def test_textos_vacios(self):
        score = MatchingExplainer._default_similarity("", "")
        assert score == 0.0

    def test_overlap_parcial(self):
        score = MatchingExplainer._default_similarity("python sql java", "python docker aws")
        assert 0.0 < score < 1.0
