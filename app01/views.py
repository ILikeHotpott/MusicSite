from io import BytesIO
import json
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models import Avg
from django import forms
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code
from app01.models import Music


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


def profile(request):
    username = request.user.username if request.user.is_authenticated else 'Guest'

    return render(request, "profile.html", {"username": username})


def profile_edit(request):
    return render(request, "profile_edit.html")
