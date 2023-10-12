from django.urls import path

from . import views

app_name = 'films'

urlpatterns = [
    path("genres/", views.GenreListView.as_view(), name='genres_list'),
    path("genre/<pk>/", views.GenreDetailView.as_view(), name='genre_detail'),
    path("binding/", views.BindingTableSerializersView.as_view(), name='binding_list'),
    path("binding/<pk>/", views.BindingTableSerializersDetailView.as_view(), name='binding_detail'),
    path("moves/", views.FilmSerializersListView.as_view(), name='move_list'),
    path("move/<pk>/", views.FilmSerializersDetailView.as_view(), name='move_detail'),
    path("ratings/", views.RatingListView.as_view(), name='all_rating'),
    path("rating/<pk>/", views.RatingDetailView.as_view(), name='rating_detail'),
]