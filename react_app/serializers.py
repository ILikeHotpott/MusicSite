from rest_framework import serializers
from react_app.models import ReactUser
from django.contrib.auth import authenticate
from react_app import models
from app01 import models as app01_models


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ReactUser
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = ReactUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    xxx = serializers.SerializerMethodField()

    class Meta:
        model = models.ReactUser
        fields = ['email', 'username', 'password', "xxx"]

    def get_xxx(self, obj):
        return "hello fucking world"


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = app01_models.UserInfo
        fields = ['id', 'username', 'avatar']


class MomentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()  # 嵌套序列化器!!

    class Meta:
        model = app01_models.Moments
        fields = "__all__"
