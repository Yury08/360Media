from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Срок действия подписки везде одинаковый, поэтому он в таблице профиля пользователя
    # Тип подписки будет храниться по ключу сессии в redise

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'Подписка типа {self.name}'
