from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('blog/', include('blog.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
                       path('__debug__/', include(debug_toolbar.urls))
                   ] + urlpatterns
