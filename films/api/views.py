from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from ..models import *
from ..services import paid_api_available
from .serializers import (BindingTableSerializers, FilmGenreSerializers,
                          FilmSerializers, RatingSerializers)


class GenreListView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = FilmGenreSerializers

    def get_queryset(self):
        return FilmGenre.objects.all() if paid_api_available(self.request.user) else 0


class GenreDetailView(generics.RetrieveAPIView, LoginRequiredMixin):
    serializer_class = FilmGenreSerializers

    def get_queryset(self):
        return FilmGenre.objects.all() if paid_api_available(self.request.user) else 0


class BindingTableSerializersView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = BindingTableSerializers

    def get_queryset(self):
        return BindingTable.objects.all() if paid_api_available(self.request.user) else 0


class BindingTableSerializersDetailView(generics.RetrieveAPIView, LoginRequiredMixin):
    serializer_class = BindingTableSerializers

    def get_queryset(self):
        return BindingTable.objects.all() if paid_api_available(self.request.user) else 0


class FilmSerializersDetailView(generics.RetrieveAPIView, LoginRequiredMixin):
    serializer_class = FilmSerializers

    def get_queryset(self):
        return Film.objects.all() if paid_api_available(self.request.user) else 0


class FilmSerializersListView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = FilmSerializers

    def get_queryset(self):
        return Film.objects.all() if paid_api_available(self.request.user) else 0


class RatingListView(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = RatingSerializers

    def get_queryset(self):
        return Rating.objects.all() if paid_api_available(self.request.user) else 0


class RatingDetailView(generics.RetrieveAPIView, LoginRequiredMixin):
    serializer_class = RatingSerializers

    def get_queryset(self):
        return Rating.objects.all() if paid_api_available(self.request.user) else 0
