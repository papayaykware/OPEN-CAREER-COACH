"""
OPEN-CAREER-COACH · tests/test_repository.py
Tests unitarios — AnalysisRepository v2.0.0-F2

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

import pytest
from pathlib import Path
from src.db.database import Database
from src.db.analysis_repository import AnalysisRepository
from src.matching.explainer import MatchingExplainer

CV_TEST   = "Ingeniero de datos con 5 años de experiencia en Python y machine learning. Máster en IA."
OFFER_TEST = "Buscamos Data Scientist con experiencia en Python. Se requiere experiencia mínima de 3 años."


@pytest.fixture
def repo(tmp_path):
    """Repositorio con base de datos temporal para cada test."""
    db   = Database(db_path=tmp_path / "test.db")
    return AnalysisRepository(db)


@pytest.fixture
def result():
    return MatchingExplainer().explain(CV_TEST, OFFER_TEST)


class TestSave:

    def test_save_devuelve_id(self, repo, result):
        id_ = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        assert isinstance(id_, int)
        assert id_ >= 1

    def test_ids_incrementales(self, repo, result):
        id1 = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        id2 = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        assert id2 > id1

    def test_save_con_export_paths(self, repo, result):
        id_ = repo.save(
            result, CV_TEST, OFFER_TEST, nivel="moderado",
            export_paths={"md": "/tmp/informe.md", "json": "/tmp/informe.json"}
        )
        rec = repo.get_by_id(id_)
        assert rec.export_md   == "/tmp/informe.md"
        assert rec.export_json == "/tmp/informe.json"


class TestGetById:

    def test_get_existente(self, repo, result):
        id_ = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        rec = repo.get_by_id(id_)
        assert rec is not None
        assert rec.id == id_
        assert rec.global_score == result.global_score
        assert rec.narrative    == result.narrative

    def test_get_inexistente_devuelve_none(self, repo):
        assert repo.get_by_id(9999) is None

    def test_campos_json_deserializados(self, repo, result):
        id_ = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        rec = repo.get_by_id(id_)
        assert isinstance(rec.strengths,        list)
        assert isinstance(rec.gaps,             list)
        assert isinstance(rec.dimension_scores, list)
        assert isinstance(rec.gap_analysis,     list)
        assert isinstance(rec.metadata,         dict)


class TestListRecent:

    def test_lista_vacia_inicial(self, repo):
        assert repo.list_recent() == []

    def test_lista_con_registros(self, repo, result):
        repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        repo.save(result, CV_TEST, OFFER_TEST, nivel="bajo")
        recs = repo.list_recent()
        assert len(recs) == 2

    def test_orden_descendente(self, repo, result):
        id1 = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        id2 = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        recs = repo.list_recent()
        assert recs[0].id == id2  # más reciente primero

    def test_filtro_min_score(self, repo, result):
        repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        recs = repo.list_recent(min_score=0.99)
        assert len(recs) == 0

    def test_filtro_nivel(self, repo, result):
        repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        repo.save(result, CV_TEST, OFFER_TEST, nivel="bajo")
        recs = repo.list_recent(nivel="bajo")
        assert all(r.nivel == "bajo" for r in recs)

    def test_paginacion(self, repo, result):
        for _ in range(5):
            repo.save(result, CV_TEST, OFFER_TEST, nivel="moderado")
        page1 = repo.list_recent(limit=3, offset=0)
        page2 = repo.list_recent(limit=3, offset=3)
        assert len(page1) == 3
        assert len(page2) == 2


class TestStats:

    def test_stats_vacio(self, repo):
        s = repo.stats()
        assert s.get("total", 0) == 0

    def test_stats_con_datos(self, repo, result):
        repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        repo.save(result, CV_TEST, OFFER_TEST, nivel="bajo")
        s = repo.stats()
        assert s["total"] == 2
        assert s["avg_score"] is not None

    def test_stats_niveles(self, repo, result):
        repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        repo.save(result, CV_TEST, OFFER_TEST, nivel="moderado")
        repo.save(result, CV_TEST, OFFER_TEST, nivel="bajo")
        s = repo.stats()
        assert s["total_alto"]     == 1
        assert s["total_moderado"] == 1
        assert s["total_bajo"]     == 1


class TestDelete:

    def test_delete_existente(self, repo, result):
        id_ = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        assert repo.delete(id_) is True
        assert repo.get_by_id(id_) is None

    def test_delete_inexistente(self, repo):
        assert repo.delete(9999) is False

    def test_count_tras_delete(self, repo, result):
        id_ = repo.save(result, CV_TEST, OFFER_TEST, nivel="alto")
        assert repo.count() == 1
        repo.delete(id_)
        assert repo.count() == 0
