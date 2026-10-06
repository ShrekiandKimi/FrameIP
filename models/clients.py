"""Класс Client и функции работы с коллекцией клиентов."""


class Client:
    """Клиент сервиса доставки готовой еды."""

    def __init__(self, client_id: int, name: str) -> None:
        """Создать объект клиента."""
        self.id = client_id
        self.name = name

    @classmethod
    def from_data(cls, data: dict) -> "Client":
        """Создать клиента из словаря данных (например, из JSON)."""
        return cls(data["id"], data["name"])

    def __str__(self) -> str:
        """Вернуть строковое представление клиента."""
        return self.name


def add_client(clients: list[Client], name: str) -> Client:
    """Создать клиента и добавить его в коллекцию clients."""
    client_id = max((client.id for client in clients), default=0) + 1
    client = Client(client_id, name)
    clients.append(client)
    return client


def find_client_by_id(clients: list[Client], client_id: int) -> Client | None:
    """Найти клиента по идентификатору."""
    for client in clients:
        if client.id == client_id:
            return client
    return None


def find_client_by_name(clients: list[Client], name: str) -> Client | None:
    """Найти клиента по имени (без учёта регистра)."""
    name = name.lower()
    for client in clients:
        if client.name.lower() == name:
            return client
    return None


def get_or_create_client(clients: list[Client], name: str) -> Client:
    """Найти клиента по имени либо создать нового и добавить в коллекцию."""
    client = find_client_by_name(clients, name)
    if client is not None:
        return client
    return add_client(clients, name)


def show_clients(clients: list[Client]) -> None:
    """Вывести список клиентов."""
    if not clients:
        print("Клиентов пока нет.")
        return
    for client in clients:
        print(f"{client.id}. {client}")
