from django.conf import settings
from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar)),
                  ] + urlpatterns
