from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
  path('user/<pk>/', views.UserDetail.as_view(), name="user_detail"),
  path('users/', views.UserList.as_view(), name="user_list"),
]