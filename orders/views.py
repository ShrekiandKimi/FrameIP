from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

ORDERS_QUERY = """
    SELECT
        orders.id,
        orders.total,
        orders.status,
        clients.name AS client_name,
        couriers.name AS courier_name
    FROM orders
    JOIN clients ON orders.client_id = clients.id
    LEFT JOIN couriers ON orders.courier_id = couriers.id
"""


def orders(request: HttpRequest) -> HttpResponse:
    """Страница /orders/: заказы из SQLite и свободный курьер."""
    orders_data = fetch_all(ORDERS_QUERY + "ORDER BY orders.id;")
    free_courier = fetch_one(
        """
        SELECT id, name
        FROM couriers
        WHERE id NOT IN (
            SELECT courier_id
            FROM orders
            WHERE courier_id IS NOT NULL
              AND status <> 'отменён'
        )
        ORDER BY id;
        """
    )
    context = {
        "orders": orders_data,
        "free_courier": free_courier,
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Страница /orders/<id>/: карточка заказа; 404, если заказ не найден."""
    order = fetch_one(ORDERS_QUERY + "WHERE orders.id = ?;", (order_id,))

    positions = []
    if order is not None:
        positions = fetch_all(
            """
            SELECT
                dishes.name AS name,
                order_items.quantity AS quantity,
                dishes.price * order_items.quantity AS line_total
            FROM order_items
            JOIN dishes ON order_items.dish_id = dishes.id
            WHERE order_items.order_id = ?
            ORDER BY dishes.name;
            """,
            (order_id,),
        )

    context = {
        "order": order,
        "positions": positions,
    }
    return render(
        request,
        "orders/order_detail.html",
        context,
        status=404 if order is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    """Страница /orders/statistics/: агрегаты и группировки по заказам."""
    summary = fetch_one(
        """
        SELECT
            COUNT(*) AS active_orders,
            COALESCE(SUM(total), 0) AS revenue,
            COALESCE(AVG(total), 0) AS avg_total
        FROM orders
        WHERE status <> 'отменён';
        """
    )
    dishes_sold = fetch_all(
        """
        SELECT
            dishes.name AS dish_name,
            COALESCE(SUM(order_items.quantity), 0) AS sold
        FROM dishes
        LEFT JOIN order_items ON dishes.id = order_items.dish_id
        LEFT JOIN orders
            ON order_items.order_id = orders.id AND orders.status <> 'отменён'
        GROUP BY dishes.id, dishes.name
        ORDER BY sold DESC, dishes.name;
        """
    )
    clients_stats = fetch_all(
        """
        SELECT
            clients.name AS client_name,
            COUNT(orders.id) AS orders_count,
            COALESCE(SUM(orders.total), 0) AS total_sum
        FROM clients
        LEFT JOIN orders
            ON clients.id = orders.client_id AND orders.status <> 'отменён'
        GROUP BY clients.id, clients.name
        ORDER BY orders_count DESC;
        """
    )
    regular_clients = fetch_all(
        """
        SELECT
            clients.name AS client_name,
            COUNT(orders.id) AS orders_count
        FROM clients
        JOIN orders ON clients.id = orders.client_id
        WHERE orders.status <> 'отменён'
        GROUP BY clients.id, clients.name
        HAVING COUNT(orders.id) > 1
        ORDER BY orders_count DESC;
        """
    )
    context = {
        "summary": summary,
        "dishes_sold": dishes_sold,
        "clients_stats": clients_stats,
        "regular_clients": regular_clients,
    }
    return render(request, "orders/statistics.html", context)
