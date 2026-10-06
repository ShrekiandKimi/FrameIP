from django.http import HttpRequest, HttpResponse
from django.utils.html import escape


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу: кодировка, заголовок, Bootstrap и навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/dishes/">Меню</a>
        <a class="nav-link" href="/orders/">Заказы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения и навигация."""
    content = """
    <h1 class="display-4">Доставка готовой еды</h1>
    <p class="lead">Сервис заказа и доставки готовой еды.</p>
    <p>Основные разделы:</p>
    <a href="/dishes/" class="btn btn-primary me-2">Меню</a>
    <a href="/orders/" class="btn btn-secondary">Заказы</a>
    """
    return HttpResponse(page("Доставка готовой еды", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404 (подключена через handler404)."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
