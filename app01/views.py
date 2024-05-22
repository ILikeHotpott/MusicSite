from io import BytesIO
import json
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models import Avg
from django import forms
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django_redis import get_redis_connection
from app01.utils.bootstrap import BootstrapForm
from app01 import models
from app01.utils.code import check_code
from app01.models import Music, Comment, US_TopMusic, UserInfo, Playlist
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.music_api import get_ranks_songs_artists
from app01.utils import search_spotify


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
        fields = ['content']


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
            request.session.set_expiry(86400 * 30)
            return redirect("/rank_list/")
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
    user = request.user
    queryset = None
    if user.is_authenticated:
        queryset = models.Moments.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        print("form", form)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form, "queryset": queryset})


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


def rank(request, region="US"):
    # 直接从数据库中获取并按rank排序的歌曲信息
    songs_info = list(
        US_TopMusic.objects.filter(region=region).order_by('rank').values(
            'id', 'title', 'artist', 'cover_url', 'region'
        )
    )

    for song_info in songs_info:
        song_info['absolute_cover_url'] = song_info['cover_url']

    context = {
        'songs_info': songs_info,
        'region': region
    }

    return render(request, "rank.html", context)


@csrf_exempt
def upload_file_to_s3(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"error": "No file provided."}, status=400)

    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        # Construct the file name to be saved on S3
        file_name = f"uploads/{request.user.id}/{file.name}"
        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={"ContentType": file.content_type}
        )
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
        return JsonResponse({"message": "File uploaded successfully", "file_url": file_url}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def rank_api(request, region="US"):
    songs_info = get_ranks_songs_artists(11, region)
    return JsonResponse({'songs_info': songs_info})


def chat3(request):
    qq_group_num = request.GET.get("num")
    return render(request, "chat3.html", {"qq_group_num": qq_group_num})


@login_required
def chat(request):
    target_username = request.GET.get("with")
    current_username = request.user.username
    form = UserUpdateForm(instance=request.user)

    current_user_info = UserInfo.objects.get(username=current_username)
    target_user_info = UserInfo.objects.get(username=target_username)
    current_avatar_url = current_user_info.avatar.url
    target_avatar_url = target_user_info.avatar.url

    # 将用户名传递给前端模板
    return render(request, "chat.html", {
        'current_username': current_username,
        'target_username': target_username,
        'form': form,
        'current_avatar_url': current_avatar_url,
        'target_avatar_url': target_avatar_url,
    })


@csrf_exempt
def save_moment(request):
    if request.method == 'GET':
        return JsonResponse({"error": "GET method not supported"}, status=405)
    data = json.loads(request.body)
    content = data.get('content')
    image_urls_list = data.get('imageUrls', [])
    video_urls_list = data.get('videoUrls', [])
    moment = models.Moments(user=request.user, content=content, image_urls=image_urls_list, video_urls=video_urls_list)
    moment.save()
    return JsonResponse({"message": "Moment saved successfully"}, status=200)


def playground(request):
    if request.method == "GET":
        user_info = None
        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.filter(username=request.user.username).first()

        queryset = models.Moments.objects.prefetch_related('comments').all().order_by('-created_at')

        redis_conn = get_redis_connection('default')
        user_id = request.user.id if request.user.is_authenticated else None

        for moment in queryset:
            likes_key = f'post_likes:{moment.id}'
            moment.like_count = redis_conn.scard(likes_key)
            moment.is_liked = redis_conn.sismember(likes_key, user_id) if user_id else False

        return render(request, "playground.html", {"queryset": queryset, "user_info": user_info})


@login_required
@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data['post_id']
    user = request.user

    # 获取Moment实例
    moment = get_object_or_404(models.Moments, pk=post_id)

    redis_conn = get_redis_connection('default')
    likes_key = f'post_likes:{post_id}'

    already_liked = redis_conn.sismember(likes_key, user.id)

    if already_liked:
        redis_conn.srem(likes_key, user.id)
        liked = False
        moment.likes_count = redis_conn.scard(likes_key)  # 更新likes_count
    else:
        redis_conn.sadd(likes_key, user.id)
        liked = True
        moment.likes_count = redis_conn.scard(likes_key)  # 更新likes_count

    moment.save()  # 保存修改到数据库

    return JsonResponse({'liked': liked, 'like_count': moment.likes_count})


def submit_moment_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 先从ajax获取数据
            moment_id = data.get('post_id')
            comment_text = data.get('comment')

            try:
                moment = models.Moments.objects.get(id=moment_id)
            except models.Moments.DoesNotExist:
                return JsonResponse({'error': 'Moment does not exist'}, status=404)

            comment = models.MomentComment(
                user=request.user,
                moment=moment,
                content=comment_text,
            )
            comment.save()
            return JsonResponse({'message': 'Comment submitted successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def load_more_comments(request):
    post_id = request.GET.get('post_id')
    offset = int(request.GET.get('offset', 0))
    limit = 10  # 一次加载10条评论

    comments_query = models.MomentComment.objects.filter(moment_id=post_id).order_by('-created_at')
    total_comments = comments_query.count()
    comments = comments_query[offset:offset + limit]
    comments_html = render_to_string('comments_partial.html', {'comments': comments})

    # 如果当前已加载的评论（offset + 刚加载的评论数量）小于总评论数，还有更多评论
    has_more = (offset + len(comments)) < total_comments

    return JsonResponse({
        'comments_html': comments_html,
        'has_more': has_more,
        'limit': limit,
    })


def delete_post(request, post_id):
    if request.method == "POST":
        try:
            post = models.Moments.objects.get(id=post_id, user=request.user)
            post.delete()
            return JsonResponse({"success": True})
        except models.Moments.DoesNotExist:
            return JsonResponse({"success": False, "error": "Post not found or permission denied."})


def search(request):
    return render(request, "search.html")


def search_results(request):
    query = request.GET.get('query', '')
    results = search_spotify.search_spotify(query)
    return JsonResponse(results)


class CreateYourOwnChartModelForm(BootstrapModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'playlist_cover']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "John's Top 100 Playlist", 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'My favourite songs of 2024', 'class': 'form-control'}),
        }


def create_your_own_chart(request):
    if request.method == 'GET':
        form = CreateYourOwnChartModelForm()
        return render(request, "create_your_own_chart.html", {"form": form})

    form = CreateYourOwnChartModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        new_playlist = form.save(commit=False)
        new_playlist.user = request.user
        new_playlist.save()
        return redirect(f"/playlist/{new_playlist.id}")

    return render(request, "create_your_own_chart.html", {"form": form})


class SongForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'pic']


def playlist(request, playlist_id):  # 待完成，级别第三高
    playlist_info = get_object_or_404(Playlist, id=playlist_id)
    songs = playlist_info.tracks
    print("playlist_info", playlist_info)
    print("songs", songs)

    return render(request, "playlist.html", {"playlist_info": playlist_info, "songs": songs})


def rank_list(request):
    return render(request, "rank_list.html")


def home(request):  # 待完成，级别第二高
    return render(request, "home.html")


@login_required
def get_user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user).values('id', 'name')
    return JsonResponse({'playlists': list(playlists)})


@csrf_exempt
@login_required
def add_song_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        playlist_id = data.get('playlist_id')
        track_name = data.get('track_name')
        track_artist = data.get('track_artist')
        track_image = data.get('track_image')

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        music, created = Music.objects.get_or_create(
            title=track_name,
            artist=track_artist,
            defaults={'pic': track_image}
        )
        playlist.tracks.append({
            'title': track_name,
            'artist': track_artist,
            'pic_url': track_image,
            'position': playlist.track_number + 1
        })
        playlist.track_number += 1
        playlist.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def playlist_list(request):
    user = request.user
    playlists = Playlist.objects.filter(user=user).order_by('-created_at')
    return render(request, "playlist_list.html", {"playlists": playlists})
