"""Однократный перенос данных из JSON-файлов в базу SQLite."""

import json
import sqlite3

from db.database import get_connection, init_schema
from models.couriers import COURIERS

DATA_DIR = "data"
DISHES_FILE = f"{DATA_DIR}/dishes.json"
CLIENTS_FILE = f"{DATA_DIR}/clients.json"
ORDERS_FILE = f"{DATA_DIR}/orders.json"


def load_json(filename: str) -> list[dict]:
    """Прочитать JSON-файл."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn: sqlite3.Connection) -> None:
    """Очистить таблицы (сначала зависимые) для повторного импорта."""
    for table in ("order_items", "orders", "couriers", "clients", "dishes"):
        conn.execute(f"DELETE FROM {table}")


def import_dishes(conn: sqlite3.Connection, filename: str = DISHES_FILE) -> None:
    """Перенести блюда."""
    conn.executemany(
        "INSERT INTO dishes (id, name, price) VALUES (?, ?, ?)",
        [(d["id"], d["name"], d["price"]) for d in load_json(filename)],
    )


def import_clients(conn: sqlite3.Connection, filename: str = CLIENTS_FILE) -> None:
    """Перенести клиентов."""
    conn.executemany(
        "INSERT INTO clients (id, name) VALUES (?, ?)",
        [(c["id"], c["name"]) for c in load_json(filename)],
    )


def import_couriers(conn: sqlite3.Connection) -> None:
    """Перенести курьеров (в проекте они заданы списком COURIERS)."""
    conn.executemany(
        "INSERT INTO couriers (id, name) VALUES (?, ?)",
        [(courier.id, courier.name) for courier in COURIERS],
    )


def import_orders(conn: sqlite3.Connection, filename: str = ORDERS_FILE) -> None:
    """Перенести заказы и их состав (после клиентов, курьеров и блюд)."""
    orders = load_json(filename)
    conn.executemany(
        """
        INSERT INTO orders (id, client_id, courier_id, total, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (o["id"], o["client_id"], o["courier_id"], o["total"], o["status"])
            for o in orders
        ],
    )
    conn.executemany(
        """
        INSERT INTO order_items (order_id, dish_id, quantity)
        VALUES (?, ?, ?)
        """,
        [
            (o["id"], int(dish_id), quantity)
            for o in orders
            for dish_id, quantity in o["items"].items()
        ],
    )


def import_all(conn: sqlite3.Connection) -> None:
    """Выполнить весь импорт в порядке, учитывающем внешние ключи."""
    clear_tables(conn)
    import_dishes(conn)
    import_clients(conn)
    import_couriers(conn)
    import_orders(conn)


def main() -> None:
    """Создать схему и перенести данные одной транзакцией."""
    conn = get_connection()
    try:
        init_schema(conn)
        import_all(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
