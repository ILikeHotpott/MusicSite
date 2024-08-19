from react_app import models
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework.views import APIView
from rest_framework.response import Response
from react_app.serializers import UserSerializer
from react_app.throttle import IPRateThrottle, UserRateThrottle
from react_app.redis_connection import redis_client


class TestView(APIView):
    # throttle_classes = [IPRateThrottle, UserRateThrottle]  # 一旦有一个超过，就会限流
    # versioning_class = AcceptHeaderVersioning  # 版本控制
    #
    # parser_classes = [JSONParser, FormParser, MultiPartParser]  # 有上传文件用MultiPartParser
    # content_negotiation_class = DefaultContentNegotiation
    def get(self, request):
        return Response({'haha': '123'})

    def post(self, request):
        print(request.data)
        return Response(request.data)


class UserView(APIView):

    def get(self, request):
        queryset = models.ReactUser.objects.all()
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class RedisAddTestView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user_name = request.GET.get('user_name')
        user_score = request.GET.get('user_score')

        key = f"user:{user_id}"
        redis_client.hset(key, mapping={
            "name": user_name,
            "score": user_score
        })

        return Response({'status': 'success', 'user_id': user_id, 'user_name': user_name, 'user_score': user_score})


class RedisGetTestView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        key = f"user:{user_id}"
        user_data = redis_client.hgetall(key)
        if user_data:
            return Response({'status': 'success', 'user_data': user_data})
        else:
            return Response({'status': 'failed', 'user_id': user_id})

