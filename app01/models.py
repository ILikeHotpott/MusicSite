from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Music(models.Model):
    pic = models.FileField(verbose_name="Logo", max_length=128, upload_to="album/", null=True, blank=True)
    title = models.CharField(max_length=64, verbose_name='Title', null=True, blank=True)
    artist = models.CharField(max_length=64, verbose_name='Artist', null=True, blank=True)
    weeks = models.IntegerField(verbose_name='Weeks', null=True, blank=True)
    number_of_votes = models.IntegerField(default=0, verbose_name='Number of Votes')
    total_score = models.FloatField(max_length=10, default=0.0, verbose_name='Total Score')

    def average_score(self):
        if self.number_of_votes == 0:
            return 0
        return round(self.total_score / self.number_of_votes, 1)


class UserInfo(AbstractUser):
    username = models.CharField(max_length=32, verbose_name='username', unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    age = models.IntegerField(verbose_name='age')
    profile_info = models.CharField(max_length=256, verbose_name='profile_info', null=True, blank=True)
    avatar = models.FileField(max_length=256, verbose_name='avatar', upload_to="avatar/", null=True, blank=True,
                              default='profile/default.png')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age']


class Rating(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name='Music')
    score = models.FloatField(max_length=5, verbose_name='Score')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Rating time')

    class Meta:
        unique_together = (('user', 'music'),)

    def __str__(self):
        return f'{self.user.username} rated {self.music.title} as {self.score}'


class Comment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User', related_name='comments')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name='Music', related_name='comments')
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')


class Chart(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Chart Name')
    description = models.TextField(blank=True, verbose_name='Description')


class US_TopMusic(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    rank = models.IntegerField(default=0)
    region_choices = (
        ('US', 'United States'),
        ('UK', 'British'),
        ('AU', 'Australia'),
    )
    region = models.CharField(max_length=2, choices=region_choices, default='US')
    album_name = models.CharField(max_length=255, null=True, blank=True)


class Moments(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User')
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')
    image_urls = models.JSONField(default=list, verbose_name='Image URLs')
    video_urls = models.JSONField(default=list, verbose_name='Video URLs')
    likes_count = models.IntegerField(default=0, verbose_name="Likes Count")


class Like(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_likes')
    moment = models.ForeignKey(Moments, on_delete=models.CASCADE, related_name='moment_likes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Liked At')

    class Meta:
        unique_together = ('user', 'moment')


class MomentComment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User', related_name='moment_comments')
    moment = models.ForeignKey(Moments, on_delete=models.CASCADE, verbose_name='Moment', related_name='comments')
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name='Parent Comment')

    class Meta:
        verbose_name = 'Moment Comment'
        verbose_name_plural = 'Moment Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.moment.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def is_reply(self):
        """Check if the comment is a reply to another comment."""
        return self.parent is not None


class Playlist(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User', related_name='playlists')
    name = models.CharField(max_length=128, verbose_name='Playlist Name')
    description = models.TextField(verbose_name='Description', blank=True)
    playlist_cover = models.ImageField(max_length=512, verbose_name='playlist_cover', upload_to="playlist_cover/",
                                       null=True,
                                       blank=True,
                                       default='https://musictop-bucket.s3.ap-southeast-2.amazonaws.com/default.jpeg')
    track_number = models.PositiveIntegerField(verbose_name='Track Number', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return f"{self.name} by {self.user.username}"

    def id(self):
        return self.id


class PlaylistMusic(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, verbose_name='Playlist', related_name='tracks')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name='Music')
    position = models.PositiveIntegerField(verbose_name='Track Position', default=1)

    class Meta:
        unique_together = ('playlist', 'music')
        ordering = ['position']

    def __str__(self):
        return f"{self.music.title} in {self.playlist.name} at position {self.position}"