import json
import re
import sqlite3
from pathlib import Path

import pytest

from db.database import SCHEMA_PATH, get_connection, init_schema
from db.import_json import import_all

BASE_DIR = Path(__file__).resolve().parent.parent
QUERIES_PATH = BASE_DIR / "sql" / "queries.sql"


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.chdir(BASE_DIR)
    connection = get_connection(tmp_path / "test.sqlite")
    init_schema(connection)
    import_all(connection)
    connection.commit()
    yield connection
    connection.close()


def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_schema_creates_all_tables(conn):
    tables = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert {"dishes", "clients", "couriers", "orders", "order_items"} <= tables


def test_schema_is_idempotent(conn):
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_import_matches_json(conn):
    for table, filename in (
        ("dishes", "dishes.json"),
        ("clients", "clients.json"),
        ("orders", "orders.json"),
    ):
        with open(BASE_DIR / "data" / filename, encoding="utf-8") as file:
            assert count(conn, table) == len(json.load(file))


def test_repeated_import_does_not_duplicate(conn):
    import_all(conn)
    assert count(conn, "dishes") == 3


def test_foreign_keys_are_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO orders (id, client_id, courier_id, total, status)"
            " VALUES (99, 999, NULL, 100, 'в обработке')"
        )


def test_parameterized_search(conn):
    rows = conn.execute(
        "SELECT name FROM dishes WHERE price <= ? ORDER BY price", (450,)
    ).fetchall()
    assert [row["name"] for row in rows] == ["Салат Цезарь", "Ролл Калифорния"]


def test_injection_is_not_executed(conn):
    rows = conn.execute(
        "SELECT id FROM dishes WHERE name = ?", ("x' OR '1'='1",)
    ).fetchall()
    assert rows == []


def test_all_queries_from_file_run(conn):
    text = re.sub(r"^--.*$", "", QUERIES_PATH.read_text(encoding="utf-8"), flags=re.M)
    queries = [part.strip() for part in text.split(";") if part.strip()]
    assert len(queries) >= 10
    for query in queries:
        conn.execute(query).fetchall()


def test_group_by_keeps_dishes_without_orders(conn):
    rows = conn.execute(
        """
        SELECT dishes.name, COALESCE(SUM(order_items.quantity), 0) AS sold
        FROM dishes
        LEFT JOIN order_items ON dishes.id = order_items.dish_id
        GROUP BY dishes.id, dishes.name
        """
    ).fetchall()
    assert len(rows) == 3
    assert sorted(row["sold"] for row in rows) == [0, 0, 2]
