from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Music(models.Model):
    pic = models.FileField(verbose_name="Logo", max_length=128, upload_to="album/", null=True, blank=True)
    title = models.CharField(max_length=64, verbose_name='Title', null=True, blank=True)
    artist = models.CharField(max_length=64, verbose_name='Artist', null=True, blank=True)
    weeks = models.IntegerField(verbose_name='Weeks',null=True, blank=True)
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age']


class Rating(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='User')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name='Music')
    score = models.FloatField(max_length=5, verbose_name='Score')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Rating time')

    def __str__(self):
        return f'{self.user.username} rated {self.music.title} as {self.score}'