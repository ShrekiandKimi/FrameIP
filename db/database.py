"""Подключение к базе данных SQLite и выполнение запросов."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "frameip.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение: поля результата доступны по именам."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Создать таблицы из sql/schema.sql (повторный запуск безопасен)."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()


def fetch_all(query: str, params: tuple = ()) -> list[sqlite3.Row]:
    """Выполнить SELECT с параметрами ? и вернуть все строки."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()) -> sqlite3.Row | None:
    """Выполнить SELECT с параметрами ? и вернуть одну строку или None."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()
