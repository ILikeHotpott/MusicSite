from react_app import models
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework.views import APIView
from rest_framework.response import Response
from react_app.serializers import UserSerializer
from react_app.throttle import IPRateThrottle, UserRateThrottle


class TestView(APIView):
    throttle_classes = [IPRateThrottle, UserRateThrottle]  # 一旦有一个超过，就会限流
    versioning_class = AcceptHeaderVersioning  # 版本控制

    parser_classes = [JSONParser, FormParser, MultiPartParser]  # 有上传文件用MultiPartParser
    content_negotiation_class = DefaultContentNegotiation

    def get(self, request):
        print(request.version)
        print(request.versioning_scheme)
        url = request.versioning_scheme.reverse("test", request=request, format=None)
        print(url)
        return Response({'haha': '123'})

    def post(self, request):
        print(request.data)
        return Response("OK")


class UserView(APIView):

    def get(self, request):
        queryset = models.ReactUser.objects.all()
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data)
