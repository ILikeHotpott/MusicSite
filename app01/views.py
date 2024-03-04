from io import BytesIO
import json
import queue
import time
import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models import Avg
from django.core.cache import cache
from django.db.models import Q
from django import forms
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from djangoProject.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, MUSIXMATCH_API_KEY
from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm
from app01 import models
from app01.utils.code import check_code
from app01.models import Music, Comment, US_TopMusic
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.music_api import get_ranks_songs_artists, get_album_cover, remove_feat, remove_parentheses


class MusicModelForm(BootstrapModelForm):
    class Meta:
        model = Music
        fields = ["pic", "title", "artist", "weeks"]


def charts(request):
    queryset = models.Music.objects.annotate(average_score=Avg('rating__score')).order_by('-average_score')
    for music in queryset:
        music.avg_score = music.average_score
    if request.method == "GET":
        return render(request, "charts.html", {"queryset": queryset})


def charts_add(request):
    if request.method == "GET":
        form = MusicModelForm()
        return render(request, "charts_add.html", {"form": form})

    form = MusicModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/charts/")

    return render(request, "charts.html", {"form": form})


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = models.Music
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # 仅需要用户填写评论内容


def charts_comment(request, nid):
    music = get_object_or_404(Music, id=nid)
    comments = Comment.objects.filter(music=music).select_related('user').order_by('-created_at')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            new_comment = comment_form.save(commit=False)
            new_comment.music = music
            new_comment.user = request.user
            new_comment.save()
            # 使用reverse时，确保视图名称与urls.py中定义的名称一致
            return redirect(reverse('charts_comment', kwargs={'nid': nid}))
    else:
        comment_form = CommentForm()

    average_score = music.average_score()

    return render(request, "charts_comment.html", {
        "music": music,
        "comments": comments,
        "comment_form": comment_form,
        "average_score": average_score,
    })


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        required=True
    )
    code = forms.CharField(
        label="",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        return self.cleaned_data.get("password")


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Incorrect code")
            return render(request, "login.html", {"form": form})

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/charts/")
        else:
            form.add_error("password", "Incorrect username or password")
            return render(request, "login.html", {"form": form})
    else:
        return render(request, "login.html", {"form": form})


def image_code(request):
    img, code_string = check_code()

    # write the code to session
    request.session["image_code"] = code_string
    # the code would expire in 60 seconds
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, "PNG")
    stream.getvalue()

    return HttpResponse(stream.getvalue(), content_type="image/png")


class RegisterModelForm(BootstrapModelForm):
    username = forms.CharField(label="", widget=forms.TextInput)
    password = forms.CharField(label="", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(render_value=True)
    )
    age = forms.IntegerField(label="", widget=forms.NumberInput)
    code = forms.CharField(label="", widget=forms.TextInput)

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'age', 'code']

    def clean_password(self):
        return self.cleaned_data.get("password")

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Inconsistent password")
        return confirm_password


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # 进行其他注册后处理，比如自动登录用户、重定向等
        return redirect("/login/")

    return render(request, "register.html", {"form": form})


def logout(request):
    """ logout """
    request.session.clear()

    return redirect("/charts/")


@require_POST
@login_required
def rate_music(request):
    if request.user.is_authenticated:
        print("already logged in")
    else:
        print("not yet logged in")

    if request.method == 'POST':
        data = json.loads(request.body)
        music_id = data.get('musicId')
        score = float(data.get('score'))
        user = request.user

        music = get_object_or_404(models.Music, id=music_id)
        rating, created = models.Rating.objects.update_or_create(
            user=user, music=music,
            defaults={'score': score}
        )

        if created:
            music.number_of_votes += 1
            music.total_score += score
        else:
            old_score = rating.score
            music.total_score = music.total_score - old_score + score

        music.save()

    return redirect("/charts/")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['username', 'age', 'profile_info', 'avatar']


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        print("form", form)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form})


def profile_edit(request):
    return render(request, "profile.html", {"user": request.user})


class UserAvatarForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['avatar']


@login_required
def profile_avatar(request):
    if request.method == 'POST':
        form = UserAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UserAvatarForm(instance=request.user)

    return render(request, "profile_edit.html", {'form': form})


def download_image(image_url, local_path):
    """下载图片并保存到本地路径。如果下载失败，返回False。"""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")
    return False


def rank(request, region="US"):
    last_update_timestamp = cache.get(f'last_update_{region}')
    current_timestamp = time.time()

    if not last_update_timestamp or (current_timestamp - last_update_timestamp >= 86400):
        songs_info = get_ranks_songs_artists(50, region)
        added_songs = 0

        for song_info in songs_info:
            if added_songs >= 100:  # 如果已经成功添加了100首歌，结束循环
                break
            rank, song, artist = song_info
            song = remove_parentheses(song)
            artist = remove_feat(artist)
            if US_TopMusic.objects.filter(title=song, artist=artist).exists():
                continue  # 如果存在，跳过当前循环迭代

            image_filename = f"{rank}_{song}_{artist}.jpg".replace(" ", "_").replace("/", "_")
            local_image_path = os.path.join(settings.MEDIA_ROOT, 'album', image_filename)

            cover_url = get_album_cover(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, song, artist)
            if not os.path.exists(local_image_path):
                if not download_image(cover_url, local_image_path):
                    relative_image_path = 'album/default.jpeg'
                else:
                    relative_image_path = os.path.join('album', image_filename)
            else:
                relative_image_path = os.path.join('album', image_filename)

            # Update or create the entry
            US_TopMusic.objects.update_or_create(
                title=song, artist=artist,
                defaults={'cover_url': relative_image_path}
            )
            added_songs += 1

        cache.set(f'last_update_{region}', current_timestamp, None)

    enhanced_songs_info = list(US_TopMusic.objects.filter(region=region).values('id', 'title', 'artist', 'cover_url', 'region'))
    for song_info in enhanced_songs_info:
        song_info['absolute_cover_url'] = settings.MEDIA_URL + song_info['cover_url']

    context = {
        'songs_info': enhanced_songs_info,
        'region': region
    }

    return render(request, "rank.html", context)


def chat(request):
    return render(request, "chat.html")


DB = []


def send_msg(request):
    text = request.GET.get("text")
    DB.append(text)
    return HttpResponse("OK")


def get_msg(request):
    index = request.GET.get("index")
    index = int(index)
    context = {
        "data": DB[index:],
        "max_index": len(DB)
    }
    return JsonResponse(context)


USER_QUEUE = {}


def chat2(request):
    uid = request.GET.get("uid")
    USER_QUEUE[uid] = queue.Queue()
    return render(request, "chat2.html")


def chat3(request):
    qq_group_num = request.GET.get("num")
    return render(request, "chat3.html", {"qq_group_num": qq_group_num})