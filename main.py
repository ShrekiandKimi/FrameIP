from datetime import datetime

client_name = "Иван Петров"
dish_name = "Пицца Маргарита"
dish_price = 590.0
quantity = 2
courier_name = "Алексей Сидоров"
order_time = datetime.now()

DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 0.1
DELIVERY_COST = 150


def calculate_order_total(price, count):
    return price * count


def apply_discount(total):
    if total >= DISCOUNT_THRESHOLD:
        return total - total * DISCOUNT_RATE
    return total


def get_delivery_cost(total):
    if total >= DISCOUNT_THRESHOLD:
        return 0
    return DELIVERY_COST


def get_order_status(courier):
    if courier:
        return "заказ передан курьеру"
    else:
        return "ожидает назначения курьера"


order_total = calculate_order_total(dish_price, quantity)
discounted_total = apply_discount(order_total)
has_discount = discounted_total < order_total
delivery_cost = get_delivery_cost(discounted_total)
final_price = discounted_total + delivery_cost

print(f"Клиент: {client_name}")
print(f"Время заказа: {order_time.strftime('%H:%M')}")
print(f"Блюдо: {dish_name} x{quantity}")
print("Сумма заказа: " + str(order_total) + " руб.")
print("Скидка применена: " + ("да" if has_discount else "нет"))
print("Стоимость доставки: " + str(delivery_cost) + " руб.")
print("Итого к оплате: " + str(final_price) + " руб.")
print(f"Курьер: {courier_name}")
print(f"Статус: {get_order_status(courier_name)}")
