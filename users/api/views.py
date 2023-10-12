from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .serializers import UserSerializers


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = User.objects.all()
    serializer_class = UserSerializers