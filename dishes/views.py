from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one
from models.orders import apply_discount, get_delivery_cost


def dishes(request: HttpRequest) -> HttpResponse:
    """Страница /dishes/: список блюд из таблицы dishes (SQLite)."""
    dishes_data = fetch_all(
        """
        SELECT id, name, price
        FROM dishes
        ORDER BY name;
        """
    )
    return render(request, "dishes/dish_list.html", {"dishes": dishes_data})


def dish_detail(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Страница /dishes/<id>/: карточка блюда; 404, если блюдо не найдено."""
    dish = fetch_one(
        """
        SELECT id, name, price
        FROM dishes
        WHERE id = ?;
        """,
        (dish_id,),
    )

    context = {"dish": dish}
    if dish is not None:
        discounted_total = apply_discount(dish["price"])
        delivery_cost = get_delivery_cost(discounted_total)
        context["delivery_cost"] = delivery_cost
        context["portion_total"] = discounted_total + delivery_cost

    return render(
        request,
        "dishes/dish_detail.html",
        context,
        status=404 if dish is None else 200,
    )


def search(request: HttpRequest) -> HttpResponse:
    """Страница /dishes/search/?max_price=...: блюда не дороже заданной цены."""
    raw_price = request.GET.get("max_price", "").strip()
    max_price = None
    error = ""
    found = []

    if raw_price:
        try:
            max_price = float(raw_price.replace(",", "."))
        except ValueError:
            error = "Введите число, например 450."
        else:
            found = fetch_all(
                """
                SELECT id, name, price
                FROM dishes
                WHERE price <= ?
                ORDER BY price;
                """,
                (max_price,),
            )

    context = {
        "dishes": found,
        "max_price": raw_price,
        "searched": max_price is not None,
        "error": error,
    }
    return render(request, "dishes/search.html", context)
