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

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}, name='media'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^$', RedirectView.as_view(url='/home/', permanent=False)),

    path('accounts/', include('django.contrib.auth.urls')),
    path("charts/", views.charts),
    path("charts/add/", views.charts_add),
    path("charts/<int:nid>/comment/", views.charts_comment, name='charts_comment'),

    path("login/", views.login),
    path("logout/", views.logout),
    path("register/", views.register),
    path("image/code/", views.image_code),

    path("rate-music/", views.rate_music, name="rate_music"),

    path("rank/", views.rank, name='rank_default'),
    path('rank/<str:region>/', views.rank, name='rank_region'),
    path('rank_api/', views.rank_api),

    path("profile/", views.profile),
    path("profile/edit/", views.profile_edit),
    path('profile/avatar/', views.profile_avatar, name='profile_avatar'),

    # http://127.0.0.1/chat3/?num=123123
    path("chat3/", views.chat3),
    path("chat/", views.chat, name="chat"),

    path("playground/", views.playground),
    path("upload-to-s3/", views.upload_file_to_s3),
    path("save-moment/", views.save_moment),
    path("like-post/", views.like_post, name="like_post"),
    path("submit-moment-comment/", views.submit_moment_comment, name="submit_moment_comment"),
    path("load-more-comments/", views.load_more_comments, name="load_more_comments"),

    path("delete-post/<int:post_id>/", views.delete_post),

    path("search/", views.search, name="search"),
    path('search/results/', views.search_results, name='search_results'),
    path('create_your_own_chart/', views.create_your_own_chart, name='add_your_own_chart'),
    path('playlist/<int:playlist_id>/', views.playlist, name="playlist"),
    path('rank_list/', views.rank_list, name="rank_list"),

    path('home/', views.home, name="home"),

    path('get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),
    path('add_song_to_playlist/', views.add_song_to_playlist, name='add_song_to_playlist'),

    path('playlist_list/', views.playlist_list, name="playlist_list"),

    path('spotify-auth/', views.spotify_auth, name='spotify_auth'),
    path('spotify-callback/', views.spotify_callback, name='spotify_callback'),
    path('create-spotify-playlist/', views.create_spotify_playlist, name='create_spotify_playlist'),

    path('new_profile/', views.new_profile, name='new_profile'),

    path('api/react-login/', views.react_login, name='react_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
