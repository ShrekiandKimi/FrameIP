from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.dishes import find_dish_by_id
from models.orders import (
    apply_discount,
    calculate_order_total,
    get_delivery_cost,
)
from storage import load_dishes

DISHES_FILE = str(settings.DATA_DIR / "dishes.json")


def dishes(request: HttpRequest) -> HttpResponse:
    """Страница /dishes/: список блюд из data/dishes.json."""
    context = {
        "dishes": load_dishes(DISHES_FILE),
    }
    return render(request, "dishes/dish_list.html", context)


def dish_detail(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Страница /dishes/<id>/: карточка блюда; 404, если блюдо не найдено."""
    dishes_list = load_dishes(DISHES_FILE)
    dish = find_dish_by_id(dishes_list, dish_id)

    context = {
        "dish": dish,
    }
    if dish is not None:
        discounted_total = apply_discount(
            calculate_order_total(dishes_list, {dish.id: 1})
        )
        delivery_cost = get_delivery_cost(discounted_total)
        context["delivery_cost"] = delivery_cost
        context["portion_total"] = discounted_total + delivery_cost

    return render(
        request,
        "dishes/dish_detail.html",
        context,
        status=404 if dish is None else 200,
    )
