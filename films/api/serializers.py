from rest_framework import serializers

from users.api.serializers import UserSerializers

from ..models import *


class FilmGenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = FilmGenre
        fields = ('id', 'title', 'slug', 'icon', 'descr', 'keyword')


class FilmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'autor', 'short_story', 'full_story',
                  'xfields', 'title', 'descr', 'keywords', 'category',
                  'alt_name', 'tags', 'metatitle', 'kp_id_movie', 'year')


class BindingTableSerializers(serializers.ModelSerializer):
    genre = FilmGenreSerializers(many=True, read_only=True)
    move = FilmSerializers(read_only=True)

    class Meta:
        model = BindingTable
        fields = ('id', 'title', 'genre', 'move')


class RatingSerializers(serializers.ModelSerializer):
    film = FilmSerializers(read_only=True)
    user = UserSerializers(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'star', 'film')
