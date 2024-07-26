from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from react_app.serializers import MomentSerializer
from app01 import models
import logging


class PlaygroundView(APIView):
    def get(self, request):
        try:
            queryset = models.Moments.objects.prefetch_related('comments').all().order_by('-created_at')
            serializer = MomentSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logging.error(e)
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
