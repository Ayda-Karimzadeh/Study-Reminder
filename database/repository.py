from __future__ import annotations

from datetime import date
from sqlite3 import Row
from typing import Optional

from database.database import Database
from database.models import Topic

_ORDER_BY_CLAUSE = (
    "ORDER BY CASE WHEN next_review_date IS NULL THEN 1 ELSE 0 END, "
    "next_review_date ASC, topic_name COLLATE NOCASE ASC"
)


class TopicRepository:
    """Single point of access to topic persistence. No SQL leaks outside this class."""

    def __init__(self, database: Database) -> None:
        self._db = database

    def add_topic(self, topic_name: str) -> Topic:
        learning_date = date.today()
        stage = 0
        next_review_date = Topic.compute_next_review_date(learning_date, stage)
        cursor = self._db.connection.execute(
            "INSERT INTO topics (topic_name, learning_date, current_review_stage, next_review_date) "
            "VALUES (?, ?, ?, ?)",
            (
                topic_name,
                learning_date.isoformat(),
                stage,
                next_review_date.isoformat() if next_review_date else None,
            ),
        )
        self._db.connection.commit()
        return Topic(
            id=cursor.lastrowid,
            topic_name=topic_name,
            learning_date=learning_date,
            current_review_stage=stage,
            next_review_date=next_review_date,
        )

    def get_all_topics(self) -> list[Topic]:
        rows = self._db.connection.execute(f"SELECT * FROM topics {_ORDER_BY_CLAUSE}").fetchall()
        return [self._row_to_topic(row) for row in rows]

    def search_topics(self, query: str) -> list[Topic]:
        trimmed_query = query.strip()
        if not trimmed_query:
            return self.get_all_topics()
        rows = self._db.connection.execute(
            f"SELECT * FROM topics WHERE topic_name LIKE ? {_ORDER_BY_CLAUSE}",
            (f"%{trimmed_query}%",),
        ).fetchall()
        return [self._row_to_topic(row) for row in rows]

    def get_due_topics(self) -> list[Topic]:
        today_iso = date.today().isoformat()
        rows = self._db.connection.execute(
            "SELECT * FROM topics WHERE next_review_date IS NOT NULL AND next_review_date <= ?",
            (today_iso,),
        ).fetchall()
        return [self._row_to_topic(row) for row in rows]

    def advance_review_stage(self, topic: Topic) -> Topic:
        new_stage = topic.current_review_stage + 1
        new_next_review_date = Topic.compute_next_review_date(topic.learning_date, new_stage)
        self._db.connection.execute(
            "UPDATE topics SET current_review_stage = ?, next_review_date = ? WHERE id = ?",
            (
                new_stage,
                new_next_review_date.isoformat() if new_next_review_date else None,
                topic.id,
            ),
        )
        self._db.connection.commit()
        return Topic(
            id=topic.id,
            topic_name=topic.topic_name,
            learning_date=topic.learning_date,
            current_review_stage=new_stage,
            next_review_date=new_next_review_date,
        )

    def delete_topic(self, topic_id: int) -> None:
        self._db.connection.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        self._db.connection.commit()

    @staticmethod
    def _row_to_topic(row: Row) -> Topic:
        next_review_raw: Optional[str] = row["next_review_date"]
        return Topic(
            id=row["id"],
            topic_name=row["topic_name"],
            learning_date=date.fromisoformat(row["learning_date"]),
            current_review_stage=row["current_review_stage"],
            next_review_date=date.fromisoformat(next_review_raw) if next_review_raw else None,
        )
