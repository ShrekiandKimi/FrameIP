from models.clients import (
    add_client,
    find_client_by_name,
    get_or_create_client,
)


def test_add_client():
    clients = []
    client = add_client(clients, "Иван Петров")
    assert client.id == 1
    assert client.name == "Иван Петров"


def test_find_client_by_name_case_insensitive():
    clients = []
    add_client(clients, "Иван Петров")
    assert find_client_by_name(clients, "иван петров") is not None


def test_get_or_create_client_reuses_existing():
    clients = []
    client_1 = add_client(clients, "Иван Петров")
    client_2 = get_or_create_client(clients, "Иван Петров")
    assert client_1 is client_2
    assert len(clients) == 1


def test_get_or_create_client_creates_new():
    clients = []
    client = get_or_create_client(clients, "Мария Иванова")
    assert client.name == "Мария Иванова"
    assert len(clients) == 1
