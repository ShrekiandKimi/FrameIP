-- ==========================================
-- FrameIP: SQL-запросы проекта
-- ==========================================

-- ---------- Списки объектов ----------

-- 1. Меню: список всех блюд
SELECT id, name, price
FROM dishes
ORDER BY name;

-- 2. Список клиентов
SELECT id, name
FROM clients
ORDER BY name;

-- 3. Два самых дорогих блюда (ORDER BY + LIMIT)
SELECT id, name, price
FROM dishes
ORDER BY price DESC
LIMIT 2;

-- ---------- Фильтрация WHERE ----------

-- 4. Поиск блюд не дороже 450 руб. (в приложении значение передаётся через ?)
SELECT id, name, price
FROM dishes
WHERE price <= 450
ORDER BY price;

-- 5. Активные заказы (не отменённые)
SELECT id, client_id, courier_id, total, status
FROM orders
WHERE status <> 'отменён'
ORDER BY id;

-- 6. Заказы, которые ждут курьера (проверка NULL)
SELECT id, client_id, total
FROM orders
WHERE courier_id IS NULL
  AND status <> 'отменён';

-- ---------- Соединение таблиц JOIN ----------

-- 7. Заказы с именами клиента и курьера
SELECT
    orders.id,
    orders.total,
    orders.status,
    clients.name AS client_name,
    couriers.name AS courier_name
FROM orders
JOIN clients ON orders.client_id = clients.id
LEFT JOIN couriers ON orders.courier_id = couriers.id
ORDER BY orders.id;

-- 8. Состав заказа №1 со стоимостью позиций
SELECT
    dishes.name AS dish_name,
    order_items.quantity,
    dishes.price * order_items.quantity AS line_total
FROM order_items
JOIN dishes ON order_items.dish_id = dishes.id
WHERE order_items.order_id = 1
ORDER BY dishes.name;

-- 9. Свободные курьеры: нет активного заказа (подзапрос)
SELECT id, name
FROM couriers
WHERE id NOT IN (
    SELECT courier_id
    FROM orders
    WHERE courier_id IS NOT NULL
      AND status <> 'отменён'
)
ORDER BY id;

-- ---------- Агрегатные функции ----------

-- 10. Количество активных заказов
SELECT COUNT(*) AS active_orders
FROM orders
WHERE status <> 'отменён';

-- 11. Выручка и средний чек по активным заказам
SELECT
    COALESCE(SUM(total), 0) AS revenue,
    COALESCE(AVG(total), 0) AS avg_total
FROM orders
WHERE status <> 'отменён';

-- 12. Минимальная и максимальная цена блюда
SELECT MIN(price) AS min_price, MAX(price) AS max_price
FROM dishes;

-- ---------- Группировка GROUP BY / HAVING ----------

-- 13. Сколько порций каждого блюда заказано (блюда без заказов дают 0)
SELECT
    dishes.name AS dish_name,
    COALESCE(SUM(order_items.quantity), 0) AS sold
FROM dishes
LEFT JOIN order_items ON dishes.id = order_items.dish_id
LEFT JOIN orders
    ON order_items.order_id = orders.id AND orders.status <> 'отменён'
GROUP BY dishes.id, dishes.name
ORDER BY sold DESC, dishes.name;

-- 14. Количество активных заказов и сумма по каждому клиенту
SELECT
    clients.name AS client_name,
    COUNT(orders.id) AS orders_count,
    COALESCE(SUM(orders.total), 0) AS total_sum
FROM clients
LEFT JOIN orders
    ON clients.id = orders.client_id AND orders.status <> 'отменён'
GROUP BY clients.id, clients.name
ORDER BY orders_count DESC;

-- 15. Клиенты с более чем одним активным заказом (HAVING)
SELECT
    clients.name AS client_name,
    COUNT(orders.id) AS orders_count
FROM clients
JOIN orders ON clients.id = orders.client_id
WHERE orders.status <> 'отменён'
GROUP BY clients.id, clients.name
HAVING COUNT(orders.id) > 1
ORDER BY orders_count DESC;
