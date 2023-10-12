import json
from typing import Optional

import redis
import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import ListView

from krwz_films import settings

from .models import BindingTable, Film, FilmGenre, Reviews

# redis connect
redis_obj = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB,
                              decode_responses=True)


class GenreServicesMixin(ListView):
    def get_queryset(self):
        cache_data = cache.get('genres')
        if cache_data:
            return cache_data
        req = FilmGenre.objects.all().select_related()
        cache.set('genres', req)
        return req


class GenreDetailServicesMixin(ListView):
    def get_queryset(self):
        qs = cache.get('genre_detail')
        if qs:
            return qs
        qs = BindingTable.objects.filter(
            genre=self.kwargs['genre_pk']).prefetch_related().order_by('-move__year').select_related()
        cache.set('genre_detail', qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        object_list = list(FilmGenre.objects.filter(pk=self.kwargs["genre_pk"]).select_related().values("title"))
        ctx["title"] = object_list[0].values()
        return ctx


class FilmListServicesMixin(ListView):
    def get_queryset(self):
        return BindingTable.objects.exclude(genre__id=32).prefetch_related().order_by('-move__year').select_related()


class SeriesListServicesMixin(ListView):
    def get_queryset(self):
        # cache_data = cache.get('series_list')
        # if cache_data:
        #     return cache_data
        # requests = BindingTable.objects.filter(genre__id=32).select_related().order_by('-move__year')
        # cache.set('series_list', requests)
        return BindingTable.objects.filter(genre__id=32).prefetch_related().order_by('-move__year').select_related()


class FilmDetailServicesMixin(DetailView):
    def get_object(self, queryset=None):
        """
        Этот метод передает json с данными о фильме в шаблон, если запрос не выполнялся делаем запрос по id фильма,
        если запрос этого фильма уже был, берем данные из redis
        """
        film = Film.objects.get(id=self.kwargs.get("move_pk"))
        movie_id = film.kp_id_movie
        if redis_obj.exists(f'move_{movie_id}'):
            res_json = json.loads(redis_obj.get(f'move_{movie_id}'))
        else:
            url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{movie_id}'
            response = requests.get(url, headers={'X-API-KEY': 'a128fff4-cd06-4941-a407-0a951d5c160b',
                                                  'Content-Type': 'application/json'})
            res_json = json.loads(response.text)
            res_json['id'] = film.id
            res_json['keywords'] = film.keywords
            res_json['metatitle'] = film.metatitle

            redis_obj.set(f'move_{movie_id}', json.dumps(res_json))

        return res_json

    def get_context_data(self, **kwargs):
        """
        Этот метод выбирает все комментарии, и преобразует их в json
        """
        ctx = super().get_context_data(**kwargs)
        session = self.request.session.session_key
        key: str = session if session else get_client_ip(self.request)
        queryset = Reviews.objects.filter(film__id=self.kwargs['move_pk'], parent__isnull=True).select_related()
        commentsJson: dict = {}
        for qs in queryset:
            commentsJson[qs.id] = qs.to_json(key=key)
        ctx['comments'] = commentsJson
        return ctx


class SearchServicesMixin(ListView):
    def get_queryset(self):
        return Film.objects.filter(title__icontains=self.request.GET.get("q")).select_related()


def get_client_ip(request):
    """
    Узнает ip адрес клиента
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Что бы лайки были у одного комметария, надо сделать хеш таблиу в redis
def get_reaction(request):
    """
    Эта функция записывает реакции в redis
    """
    action: Optional[str] = request.GET.get("action")
    rev_id: Optional[str] = request.GET.get("rev_id")

    # берем за ключ сессию или ip если пользователь не авторизован
    key = request.session.session_key if request.session.session_key else get_client_ip(request)

    if action and rev_id:
        if action == 'like':
            redis_obj.incr(f'all_likes_{rev_id}')
            redis_obj.set(f'{key}_{rev_id}', f'like')
        else:
            redis_obj.decr(f'all_likes_{rev_id}')
            redis_obj.set(f'{key}_{rev_id}', f'unlike')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


def paid_api_available(user):
    """
    Проверяет какой статус подписки у пользователя и если у него оформлена подписка возвращает True
    """
    if redis_obj[f'{user}_subscription_type'] == 'API_tariff':
        return True
    else:
        raise Exception
