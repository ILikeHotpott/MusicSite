import requests
from djangoProject.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, MUSIXMATCH_API_KEY

# 示例用法
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET


def get_ranks_songs_artists(songs_num, region):
    def get_top_songs(api_key, country=region, page=1, page_size=songs_num, chart_name='top', f_has_lyrics=1):
        base_url = "http://api.musixmatch.com/ws/1.1/"
        endpoint = f"{base_url}chart.tracks.get"
        params = {
            'apikey': api_key,
            'country': country,
            'page': page,
            'page_size': page_size,
            'chart_name': chart_name,
            'f_has_lyrics': f_has_lyrics
        }

        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return "Request failed with status code: {}".format(response.status_code)

    api_key = MUSIXMATCH_API_KEY
    top_songs = get_top_songs(api_key, country=region, page=1, page_size=songs_num, chart_name='top', f_has_lyrics=1)
    track_list = top_songs["message"]["body"]["track_list"]

    info = []
    rank = 0
    for i in track_list:
        rank += 1
        song = i["track"].get("track_name")
        artist = i["track"].get("artist_name")
        clean_song = remove_parentheses(song)
        clean_artist = remove_feat(artist)

        album_name = get_album_name(client_id, client_secret, clean_song, clean_artist)

        cover_url = get_album_cover(client_id, client_secret, album_name, clean_artist) if album_name else None

        info.append([rank, song, artist, album_name, cover_url])

    return info


def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    return response.json().get('access_token')


def get_album_name(client_id, client_secret, track_name, artist_name):
    access_token = get_spotify_access_token(client_id, client_secret)
    if access_token is None:
        return None

    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': f'track:"{track_name}" artist:"{artist_name}"',
        'type': 'track',
        'limit': 1,
    }

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        if tracks:
            album_name = tracks[0].get('album', {}).get('name')
            return album_name
    return None


def get_album_cover(client_id, client_secret, album_name, artist_name):
    access_token = get_spotify_access_token(client_id, client_secret)
    if access_token is None:
        return None

    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': f'album:"{album_name}" artist:"{artist_name}"',
        'type': 'album',
        'limit': 1,
    }

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        albums = response.json().get('albums', {}).get('items', [])
        if albums:
            images = albums[0].get('images', [])
            if images:
                # 选择合适的封面图像URL
                image_url = images[0].get('url')
                return image_url  # 直接返回封面URL
    return None


def remove_feat(text):
    # 使用 'feat.' 作为分隔符分割字符串，最多分割一次
    parts = text.split("feat.", 1)
    # 返回 'feat.' 之前的部分
    return parts[0].strip()


def remove_parentheses(song):
    if "(" in song:
        index = song.index("(")
        song = song[:index - 1]
    return song