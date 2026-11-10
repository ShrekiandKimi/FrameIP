-- ==========================================
-- FrameIP: структура базы данных
-- Сервис доставки готовой еды
-- ==========================================

CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS couriers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- courier_id может быть NULL: заказ ждёт свободного курьера
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    courier_id INTEGER,
    total REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (courier_id) REFERENCES couriers(id)
);

-- состав заказа: блюдо и количество (в JSON это словарь items)
CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (order_id, dish_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);
