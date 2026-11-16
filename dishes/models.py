from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название блюда")
    price = models.FloatField(verbose_name="Цена")

    def __str__(self):
        return f"{self.name} — {self.price} руб."