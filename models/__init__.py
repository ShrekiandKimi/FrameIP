"""Пакет моделей предметной области сервиса доставки готовой еды."""

from .clients import Client
from .couriers import Courier
from .dishes import Dish
from .orders import Order

__all__ = ["Client", "Courier", "Dish", "Order"]
