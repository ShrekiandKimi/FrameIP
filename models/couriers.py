"""Класс Courier и фиксированный список курьеров сервиса."""


class Courier:
    """Курьер сервиса доставки готовой еды."""

    def __init__(self, courier_id: int, name: str) -> None:
        """Создать объект курьера."""
        self.id = courier_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление курьера."""
        return self.name


COURIERS: list[Courier] = [
    Courier(1, "Алексей Сидоров"),
    Courier(2, "Мария Кузнецова"),
    Courier(3, "Дмитрий Волков"),
]
