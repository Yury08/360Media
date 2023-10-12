# Generated by Django 4.1.5 on 2023-03-03 10:22

import django.core.validators
import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=255, verbose_name='автор')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='дата')),
                ('short_story', models.TextField(verbose_name='краткое описание фильма')),
                ('full_story', models.TextField(verbose_name='полное описание фильма')),
                ('xfields', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='название фильма')),
                ('descr', models.TextField(verbose_name='описание')),
                ('keywords', models.CharField(max_length=255, verbose_name='meta слова фильма')),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('alt_name', models.TextField()),
                ('comm_num', models.IntegerField(blank=True, null=True)),
                ('allow_comm', models.BooleanField(blank=True, default=True)),
                ('allow_main', models.BooleanField(blank=True, default=True, null=True)),
                ('approve', models.BooleanField(blank=True, default=True, null=True)),
                ('fixed', models.BooleanField(blank=True, default=False, null=True)),
                ('allow_br', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.URLField(blank=True, null=True, verbose_name='Изображение для фильма')),
                ('tags', models.CharField(max_length=255, verbose_name='теги')),
                ('metatitle', models.TextField(verbose_name='meta запрос фильма')),
                ('kp_id_movie', models.IntegerField(unique=True, verbose_name='id кинопоиска')),
                ('tags_table', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='таблица тегов')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='FilmGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название жанра')),
                ('slug', models.SlugField()),
                ('icon', models.ImageField(blank=True, default='media/default/def_img.jpg', null=True, upload_to='media/icon_genre/', verbose_name='изображение жанра')),
                ('descr', models.TextField(blank=True, verbose_name='описание жанра')),
                ('keyword', models.TextField(blank=True, max_length=400, verbose_name='meta запрос жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], verbose_name='Звёзды')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-val'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length='6000', verbose_name='Отзыв')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='re_films', to='films.film', verbose_name='Фильм')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='films.reviews', verbose_name='Родитель')),
                ('user_dislike', models.ManyToManyField(blank=True, related_name='reviews_disliked', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки')),
                ('user_like', models.ManyToManyField(blank=True, related_name='reviews_liked', to=settings.AUTH_USER_MODEL, verbose_name='Лайки')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='films', to='films.film', verbose_name='фильм')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='films.ratingstar', verbose_name='рейтинг')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='BindingTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('genre', models.ManyToManyField(related_name='genre', to='films.filmgenre')),
                ('move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='move', to='films.film')),
            ],
        ),
    ]
