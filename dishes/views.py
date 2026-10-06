from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
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
    items = ""
    for dish in load_dishes(DISHES_FILE):
        items += (
            '<li class="list-group-item d-flex justify-content-between">'
            f'<a href="/dishes/{dish.id}/">{escape(dish.name)}</a>'
            f'<span class="text-muted">{dish.price} руб.</span>'
            "</li>"
        )
    if not items:
        items = '<li class="list-group-item">Меню пусто.</li>'
    content = f"""
    <h1>Меню</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Доставка еды – меню", content))


def dish_detail(request: HttpRequest, dish_id: int) -> HttpResponse:
    """Страница /dishes/<id>/: карточка блюда; 404, если блюдо не найдено."""
    dishes_list = load_dishes(DISHES_FILE)
    dish = find_dish_by_id(dishes_list, dish_id)
    if dish is None:
        content = """
        <h1 class="text-danger">Блюдо не найдено</h1>
        <a href="/dishes/" class="btn btn-outline-secondary">
            ← к меню
        </a>
        """
        return HttpResponse(page("Блюдо не найдено", content), status=404)

    portion_total = apply_discount(calculate_order_total(dishes_list, {dish.id: 1}))
    delivery_cost = get_delivery_cost(portion_total)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(dish.name)}</h5>
            <p class="card-text"><strong>ID:</strong> {dish.id}</p>
            <p class="card-text">
                <strong>Цена:</strong> {dish.price} руб.
            </p>
            <p class="card-text">
                Заказ одной порции с доставкой:
                <span class="badge bg-primary">
                    {portion_total + delivery_cost} руб.
                </span>
                (доставка {delivery_cost} руб.)
            </p>
            <a href="/dishes/" class="btn btn-outline-secondary">
                ← к меню
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(dish.name, content), status=200)
