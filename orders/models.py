from django.db import models
from dishes.models import Dish

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя клиента")

    def __str__(self):
        return self.name

class Courier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя курьера")

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('в обработке', 'В обработке'),
        ('ожидает курьера', 'Ожидает курьера'),
        ('заказ передан курьеру', 'Передан курьеру'),
        ('отменён', 'Отменён'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Курьер")
    total = models.FloatField(verbose_name="Сумма заказа")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='в обработке', verbose_name="Статус")

    def __str__(self):
        c_name = self.courier.name if self.courier else "не назначен"
        return f"Заказ №{self.id} ({self.client.name}): {self.total} руб."