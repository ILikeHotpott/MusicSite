from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from react_app.models import ReactUser


class ReactUserProfileView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                user = ReactUser.objects.get(email=email)
                return Response({
                    'email': user.email,
                    'avatar': user.avatar.url,
                    'username': user.username,
                }, status=status.HTTP_200_OK)
            except ReactUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

