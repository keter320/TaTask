import os
import sqlite3
from datetime import datetime
from typing import List, Optional

from kivymd.app import MDApp

from models.task import Task


class DatabaseManager:
    def __init__(self):
        app = MDApp.get_running_app()
        user_data_dir = app.user_data_dir if app else os.getcwd()
        os.makedirs(user_data_dir, exist_ok=True)
        self.db_path = os.path.join(user_data_dir, "tatask.db")
        self._ensure_schema()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NULL,
                    priority INTEGER NOT NULL DEFAULT 2 CHECK(priority IN (1,2,3)),
                    deadline TEXT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT NULL,
                    is_archived INTEGER NOT NULL DEFAULT 0 CHECK(is_archived IN (0,1))
                )
                """
            )
            conn.commit()

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            deadline=row["deadline"],
            created_at=row["created_at"],
            completed_at=row["completed_at"],
            is_archived=row["is_archived"],
        )

    def create_task(self, title: str, description: Optional[str], priority: int, deadline: Optional[str]) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO tasks (title, description, priority, deadline, created_at, completed_at, is_archived)
                VALUES (?, ?, ?, ?, ?, NULL, 0)
                """,
                (title.strip(), description.strip() if description else None, priority, deadline),
            )
            conn.commit()
            return cur.lastrowid

    def get_active_tasks(self) -> List[Task]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM tasks
                WHERE is_archived = 0
                ORDER BY priority ASC, datetime(created_at) ASC
                """
            ).fetchall()
            return [self._row_to_task(r) for r in rows]

    def get_archived_tasks(self) -> List[Task]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM tasks
                WHERE is_archived = 1
                ORDER BY datetime(completed_at) DESC
                """
            ).fetchall()
            return [self._row_to_task(r) for r in rows]

    def archive_task(self, task_id: int):
        completed_at = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET is_archived = 1, completed_at = ? WHERE id = ?",
                (completed_at, task_id),
            )
            conn.commit()

    def delete_task(self, task_id: int):
        with self._connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    def clear_archive(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM tasks WHERE is_archived = 1")
            conn.commit()

    def update_task(self, task_id: int, title: str, description: Optional[str], priority: int, deadline: Optional[str]):
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, priority = ?, deadline = ?
                WHERE id = ?
                """,
                (title.strip(), description.strip() if description else None, priority, deadline, task_id),
            )
            conn.commit()
