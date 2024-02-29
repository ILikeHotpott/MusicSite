"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


from app01 import views
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}, name='media'),
    re_path(r'^$', RedirectView.as_view(url='/charts/', permanent=False)),


    path('accounts/', include('django.contrib.auth.urls')),
    path("charts/", views.charts),
    path("charts/add/", views.charts_add),

    path("login/", views.login),
    path("logout/", views.logout),
    path("register/", views.register),
    path("image/code/", views.image_code),

    path("rate-music/", views.rate_music, name="rate_music"),

    path("profile/", views.profile),
    path("profile/edit/", views.profile_edit),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
