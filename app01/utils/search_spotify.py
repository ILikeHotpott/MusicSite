from djangoProject.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
import requests
from requests.auth import HTTPBasicAuth


def get_spotify_access_token():
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        data={'grant_type': 'client_credentials'}
    )
    return auth_response.json().get('access_token')


# Spotify 搜索函数
def search_spotify(query):
    access_token = get_spotify_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    # 搜索艺术家、专辑和歌曲
    search_url = 'https://api.spotify.com/v1/search'
    params = {
        'q': query,
        'type': 'artist,album,track',
        'limit': 5
    }
    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()

    # 解析艺术家、专辑和歌曲的图片链接
    artists = [
        {'name': artist['name'], 'image': artist['images'][0]['url'] if artist['images'] else 'No image available'}
        for artist in search_results.get('artists', {}).get('items', [])
    ]
    albums = [
        {'name': album['name'], 'artist': ', '.join([artist['name'] for artist in album['artists']]),
         'image': album['images'][0]['url'] if album['images'] else 'No image available'}
        for album in search_results.get('albums', {}).get('items', [])
    ]
    tracks = [
        {
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'image': track['album']['images'][0]['url'] if track['album']['images'] else 'No image available',
            'spotify_uri': track['uri']
        }
        for track in search_results.get('tracks', {}).get('items', [])
    ]

    return {'artists': artists, 'albums': albums, 'tracks': tracks}
