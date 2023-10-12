from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView


@sync_to_async
def get_user(username):
    return User.objects.get_queryset()


class UserProfileServicesMixin(UpdateView):
    """
    Миксин для обработки профиля, передает все изображения пользователя в профиль
    """
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
