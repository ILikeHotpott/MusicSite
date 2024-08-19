import jwt
from django.contrib.auth import login
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from react_app.serializers import LoginSerializer, RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = jwt.encode({'user_id': user.id}, settings.JWT_SECRET_KEY, algorithm='HS256')
            response = Response({
                'success': 'User logged in successfully',
                'token': token
            }, status=status.HTTP_200_OK)
            response.set_cookie(key='jwt', value=token, httponly=True)
            print(response.data)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = jwt.encode({'user_id': user.id}, settings.JWT_SECRET_KEY, algorithm='HS256')
            response = Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            response.set_cookie(key='jwt', value=token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
