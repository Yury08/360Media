from asgiref.sync import sync_to_async

from .models import Subscription


def get_sub_detail(pk):
    return Subscription.objects.get(id=pk)


def get_all():
    return Subscription.objects.all().select_related()
