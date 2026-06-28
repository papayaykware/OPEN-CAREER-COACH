"""
OPEN-CAREER-COACH · src/db/database.py
Gestión de conexión SQLite — v2.0.0

Autor conceptual: Claude (Anthropic)
Director del proyecto: Javi Ciborro (@papayaykware)
Licencia: MIT
"""

from __future__ import annotations

import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger("open-career-coach.db")

DEFAULT_DB_PATH = Path("data/analyses.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    cv_text     TEXT    NOT NULL,
    offer_text  TEXT    NOT NULL,
    global_score    REAL    NOT NULL,
    nivel           TEXT    NOT NULL,
    narrative       TEXT    NOT NULL,
    strengths       TEXT    NOT NULL,  -- JSON array
    gaps            TEXT    NOT NULL,  -- JSON array
    dimension_scores TEXT   NOT NULL,  -- JSON array
    gap_analysis    TEXT    NOT NULL,  -- JSON array
    metadata        TEXT    NOT NULL,  -- JSON object
    profile_type    TEXT,
    export_md   TEXT,
    export_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_analyses_created_at
    ON analyses (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_analyses_global_score
    ON analyses (global_score DESC);
"""


class Database:
    """
    Gestiona la conexión y el esquema SQLite.

    Uso:
        db = Database()
        with db.connection() as conn:
            conn.execute("SELECT * FROM analyses")
    """

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        with self.connection() as conn:
            conn.executescript(SCHEMA)
        logger.info(f"Base de datos inicializada en {self.db_path}")

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager que garantiza commit/rollback y cierre."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")   # mejor concurrencia
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error en transacción SQLite: {e}")
            raise
        finally:
            conn.close()
