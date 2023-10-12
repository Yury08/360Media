from django.shortcuts import redirect, render
from django.urls import reverse

from subscription.services import get_sub_detail

from .forms import OrderForm
from .services import order_create_services


def order_create(request):
    if request.method == 'POST':
        form = order_create_services(request)
        # return render(request, 'orders/created.html', {"form": form})
        return redirect(reverse("payment:process"))
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {"form": form, "sub": get_sub_detail(1)})
