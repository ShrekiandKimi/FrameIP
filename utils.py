"""Вспомогательные функции безопасного ввода данных."""


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя дробное число, повторяя запрос при ошибке."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите число (например, 350 или 350.5).")
