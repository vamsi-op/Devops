# database.py
# This file keeps all SQLite operations in one place so app.py stays clean.

import os
import sqlite3
from typing import List, Dict

# Build an absolute path to feedback.db in the project root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "feedback.db")


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection with dictionary-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the feedback table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_feedback(name: str, message: str) -> None:
    """Insert a single feedback entry into the database."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO feedback (name, message) VALUES (?, ?)",
            (name, message),
        )
        conn.commit()


def get_all_feedback() -> List[Dict]:
    """Return all feedback entries, newest first."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, message, created_at FROM feedback ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_recent_feedback(limit: int = 5) -> List[Dict]:
    """Return the latest feedback entries for quick display on the home page."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, message, created_at
            FROM feedback
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
