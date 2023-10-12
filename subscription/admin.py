from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'price')
    list_display_links = ('name',)
