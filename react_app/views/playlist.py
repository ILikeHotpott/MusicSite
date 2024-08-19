from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from react_app.models import Playlist


class PlaylistView(APIView):
    def get(self, request, id):
        # 获取指定ID的歌单
        playlist = Playlist.objects.filter(id=id).annotate(
            playlist_name=F('name'),
            title=F('tracks__title'),
            artist=F('tracks__artist'),
            pic_url=F('tracks__pic_url'),
        ).values(
            'playlist_name', 'title', 'artist', 'pic_url', 'playlist_cover'
        )

        if not playlist.exists():
            return Response({'error': 'Playlist not found'}, status=404)

        return Response(list(playlist))
