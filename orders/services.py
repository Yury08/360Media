from subscription.models import Subscription

from .forms import OrderForm
from .models import OrderItem


def order_create_services(request):
    """
    Эта функция создает заказ на оформление подписки
    """
    sub = Subscription.objects.get(id=1)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save()
        request.session['order_id'] = order.id
        OrderItem.objects.create(order=order, type_of_subscription=sub, price=sub.price)
    return form
