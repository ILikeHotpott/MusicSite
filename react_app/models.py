from django.contrib.auth.models import AbstractUser
from app01.models import PlaylistItem
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class ReactUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    avatar = models.FileField(max_length=256, verbose_name='avatar', upload_to="avatar/", null=True, blank=True,
                              default='profile/default.png')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


# class PlaylistItem(models.Model):
#     title = models.CharField(max_length=256, verbose_name='Title')
#     artist = models.CharField(max_length=128, verbose_name='Artist')
#     pic_url = models.URLField(max_length=512, verbose_name='Picture URL', null=True, blank=True)
#     spotify_uri = models.CharField(max_length=64, verbose_name='Spotify URI', unique=True, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['spotify_uri']),
#         ]
class Playlist(models.Model):
    user = models.ForeignKey(ReactUser, on_delete=models.CASCADE, verbose_name='User', related_name='react_playlists')
    name = models.CharField(max_length=128, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, default='')
    playlist_cover = models.URLField(max_length=512, verbose_name='playlist_cover', null=True, blank=True,
                                     default='https://musictop-bucket.s3.ap-southeast-2.amazonaws.com/default.jpeg')
    tracks = models.ManyToManyField(PlaylistItem, related_name='react_playlists', blank=True)
    track_number = models.PositiveIntegerField(verbose_name='Track Number', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def save(self, *args, **kwargs):
        self.track_number = self.tracks.count()
        super().save(*args, **kwargs)
