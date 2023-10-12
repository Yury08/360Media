import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from subscription.models import Subscription

from .forms import CommentForm, RatingForm
from .models import Film, FilmGenre, Rating, Reviews
from .services import (FilmDetailServicesMixin, FilmListServicesMixin,
                       GenreDetailServicesMixin, GenreServicesMixin,
                       SearchServicesMixin, SeriesListServicesMixin,
                       get_reaction)

# redis connect
redis_obj = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB,
                              decode_responses=True)


# seo
class SitemapXmlView(TemplateView):
    template_name = 'sitemapxml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['films'] = Film.objects.all()
        ctx['genres'] = FilmGenre.objects.all()
        return ctx

# footer nav template
def about(request):
    return render(request, "footer/about.html")


def our_services(request):
    return render(request, "footer/our_services.html")


def privacy_policy(request):
    return render(request, "footer/privacy_policy.html")


def status(request):
    if request.user.is_authenticated:
        user_status = redis_obj[f'{request.user}_subscription_type']
    else:
        user_status = "default"
    return render(request, "footer/status.html", {"status": user_status})


def faq(request):
    return render(request, "footer/faq.html")


@login_required
def paid_api(request):
    if redis_obj[f'{request.user}_subscription_type'] == 'default':
        sub = Subscription.objects.get(id=1)
        return render(request, "footer/paid_api.html", {"sub": sub})
    elif redis_obj[f'{request.user}_subscription_type'] == 'API_tariff':
        return render(request, "footer/paid_api.html", {"sub": False})


def error404(request, exception):
    """
    404 Not Found
    """
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err404.html', {'word': word,
                                                  'title': 'Not Found'})


def error500(request):
    """
    500 Internal
    """
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err500.html', {'word': word,
                                                  'title': 'Internal'})


def error403(request, exception):
    """
    403 Forbidden
    """
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err403.html', {'word': word,
                                                  'title': 'Forbidden'})


def error400(request, exception):
    """
    400 Bad Request
    """
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err400.html', {'word': word,
                                                  'title': 'Bad Request'})


class Main(ListView):
    template_name = 'films/main.html'
    model = Subscription
    context_object_name = 'subscription'


class GenreView(GenreServicesMixin):
    template_name = 'films/genres.html'
    context_object_name = 'genres'


class GenreDetail(GenreDetailServicesMixin):
    template_name = 'films/genre_detail.html'
    context_object_name = 'films'
    paginate_by = 15


class FilmList(FilmListServicesMixin):
    template_name = 'films/films_list.html'
    context_object_name = 'films'
    paginate_by = 30


class SeriesList(SeriesListServicesMixin):
    template_name = 'films/series_list.html'
    context_object_name = 'series'
    paginate_by = 30


class FilmDetail(FilmDetailServicesMixin):
    template_name = 'films/film_detail.html'
    context_object_name = 'film'
    extra_context = {'rating_form': RatingForm()}
    login_url = 'users:reg'


class AddReview(View):
    @staticmethod
    def post(request, pk):
        form = CommentForm(request.POST)
        film = Film.objects.get(id=pk)
        if form.is_valid():
            cd = form.cleaned_data
            if request.POST.get('parent'):
                Reviews.objects.create(name=cd['name'],
                                       text=cd['text'],
                                       film=film,
                                       parent_id=int(request.POST.get('parent')))
            else:
                Reviews.objects.create(name=cd['name'],
                                       text=cd['text'],
                                       film=film)
            return redirect('films:film_detail', pk)
        return JsonResponse({'success': True})


class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=User.objects.get(),
                film=Film.objects.get(id=int(request.POST.get("movie"))),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class Search(SearchServicesMixin):
    template_name = 'films/search_list.html'
    context_object_name = 'films'


def reaction(request):
    get_reaction(request)
    return HttpResponse(status=200)
