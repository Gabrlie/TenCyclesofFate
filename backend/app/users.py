"""
Database helpers for managing local application accounts.
Supports both SQLite and MySQL backends via the shared get_db_connection.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import sqlite3
import mysql.connector

from .db import get_db_connection
logger = logging.getLogger(__name__)


@contextmanager
def _managed_connection():
    conn = get_db_connection()
    if conn is None:
        raise RuntimeError("Database connection unavailable")
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:  # pragma: no cover - defensive close
            logger.exception("Failed to close database connection")


def init_user_table() -> None:
    """Ensure the users table exists in the configured database."""
    with _managed_connection() as conn:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name TEXT,
                    trust_level INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        elif isinstance(conn, mysql.connector.MySQLConnection):
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(191) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name VARCHAR(191),
                    trust_level INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) CHARACTER SET utf8mb4
                """
            )
            conn.commit()
        else:  # pragma: no cover - defensive
            raise RuntimeError("Unsupported database connection type")


@dataclass
class UserRecord:
    id: int
    username: str
    password_hash: str
    display_name: str | None
    trust_level: int
    created_at: datetime | None


def create_user(
    *,
    username: str,
    password_hash: str,
    display_name: str | None = None,
    trust_level: int = 0,
) -> UserRecord:
    """Insert a new local account."""
    with _managed_connection() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, password_hash, display_name, trust_level)
            VALUES (%s, %s, %s, %s)
        """
        params: tuple[Any, ...]
        if isinstance(conn, sqlite3.Connection):
            query = query.replace("%s", "?")
            params = (username, password_hash, display_name, trust_level)
        else:
            params = (username, password_hash, display_name, trust_level)

        try:
            cursor.execute(query, params)
            conn.commit()
        except (sqlite3.IntegrityError, mysql.connector.IntegrityError) as exc:
            logger.info("Username %s already exists", username)
            raise ValueError("用户名已存在") from exc

        user_id = cursor.lastrowid
        return UserRecord(
            id=user_id,
            username=username,
            password_hash=password_hash,
            display_name=display_name,
            trust_level=trust_level,
            created_at=datetime.now(),
        )


def get_user_by_username(username: str) -> UserRecord | None:
    """Fetch a user record by username."""
    with _managed_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id, username, password_hash, display_name, trust_level, created_at
            FROM users
            WHERE username = %s
        """
        params: tuple[Any, ...]
        if isinstance(conn, sqlite3.Connection):
            query = query.replace("%s", "?")
            params = (username,)
        else:
            params = (username,)

        cursor.execute(query, params)
        row = cursor.fetchone()
        if not row:
            return None

        # mysql returns tuples, sqlite may return tuple as well
        return UserRecord(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            display_name=row[3],
            trust_level=row[4],
            created_at=row[5],
        )
