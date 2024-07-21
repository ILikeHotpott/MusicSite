from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ReactUser


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = ReactUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except ReactUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ReactUser.objects.get(pk=user_id)
        except ReactUser.DoesNotExist:
            return None


class MyAuthentication(BaseAuthentication):

    # 做用户验证
    # 1. 读取请求传递的token
    # 2. 验证token是否有效
    # 3. 返回值
    #    3.1  返回tuple 认证成功 request.user    request.auth
    #    3.2  抛出异常   认证失败 -> 返回错误信息
    #    3.3  返回None  多个认证类 [class1, class2, class3]
    def authenticate(self, request):
        token = request.query_params.get('token')
        if token:
            return "yitong", token
        raise AuthenticationFailed({"code": 20000, "error": "Authentication failed"})