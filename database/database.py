from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union


class Database:
    """Owns the SQLite connection and schema for the application."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_name TEXT NOT NULL,
        learning_date TEXT NOT NULL,
        current_review_stage INTEGER NOT NULL DEFAULT 0,
        next_review_date TEXT,
        last_notified_date TEXT
    );
    """

    def __init__(self, db_path: Union[str, Path]) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.execute(self.SCHEMA)
        self._run_migrations()

    def _run_migrations(self) -> None:
        """Adds columns introduced after the initial release to existing databases."""
        existing_columns = {
            row["name"] for row in self._connection.execute("PRAGMA table_info(topics)").fetchall()
        }
        if "last_notified_date" not in existing_columns:
            with self._connection:
                self._connection.execute("ALTER TABLE topics ADD COLUMN last_notified_date TEXT")

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    def close(self) -> None:
        self._connection.close()
