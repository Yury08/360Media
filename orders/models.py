from django.db import models

from subscription.models import Subscription


class Order(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-created', )

    def __str__(self):
        return f"Заказ {self.id}"



# Такая архитектура не случайна, сейчас в бд всего одна подписка,
# но если их будет больше, то такая архитектура легок масштабируется
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    type_of_subscription = models.ForeignKey(Subscription,
                                             related_name="order_sub_item",
                                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Subscription {self.id}'
