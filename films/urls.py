from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'films'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('genres/', views.GenreView.as_view(), name='genres'),
    path('genres/<int:genre_pk>/', views.GenreDetail.as_view(), name='genres_detail'),
    path('film/<int:move_pk>/', views.FilmDetail.as_view(), name='film_detail'),
    path('films/', views.FilmList.as_view(), name='films_list'),
    path('series/', views.SeriesList.as_view(), name='series_list'),
    path('search/', views.Search.as_view(), name='search'),
    # Рейтинг
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    # Отзыв
    path("reaction/", views.reaction, name="reaction"),
    path('review/<pk>/', views.AddReview.as_view(), name='add_review'),
    # footer nav template
    path('about/', views.about, name='about'),
    path('our_services/', views.our_services, name='our_services'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('status/', views.status, name='status'),
    path('faq/', views.faq, name='faq'),
    path('paid_api/', views.paid_api, name='paid_api'),
    # sitemap, seo
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', views.SitemapXmlView.as_view(), name="sitemap")
]
