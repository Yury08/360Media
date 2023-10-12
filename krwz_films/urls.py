from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    # path('payment/', include('payment.urls', namespace='payment')),
    path('', include('films.urls', namespace='films')),
    path('move_api/', include('films.api.urls', namespace='move_api')),
    path('user_api/', include('users.api.urls', namespace='user_api')),
]

"""
    400 Bad Request
    403 Forbidden
    404 Not Found
    500 Internal
"""

handler400 = 'films.views.error400'
handler403 = 'films.views.error403'
handler404 = 'films.views.error404'
handler500 = 'films.views.error500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
