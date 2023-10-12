import datetime

from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='default/def_img.jpg', upload_to='user_images')
    # Подписка. Время действия
    subscriptionTime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def has_paid(self, current_date=datetime.datetime.today()):
        """
        Проверяем, когда у пользователя закончиться подписка
        """
        return current_date < self.subscriptionTime

    def save(self, *args, **kwargs):
        """
        Обрезает изображение пользователя
        """
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профаил'
        verbose_name_plural = 'Профайлы'
