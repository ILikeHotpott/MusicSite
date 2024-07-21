from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ReactUserProfileView(APIView):
    def get(self, request):
        return Response({'id': '1234567890', 'message': 'Hello baby'}, status=status.HTTP_200_OK)