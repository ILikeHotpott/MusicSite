import requests
from djangoProject.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, MUSIXMATCH_API_KEY
from django.core.cache import cache

# 示例用法
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET


def get_ranks_songs_artists(songs_num, region):
    cache_key = f'songs_info_{region}_{songs_num}'
    cached_songs_info = cache.get(cache_key)
    if cached_songs_info:
        return cached_songs_info

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

    # 示例：获取美国的顶部歌曲列表
    top_songs = get_top_songs(api_key, country=region, page=1, page_size=songs_num, chart_name='top', f_has_lyrics=1)

    a = top_songs["message"]["body"]["track_list"]  # list

    info = []
    # 获取歌曲的名字
    rank = 0
    for i in a:
        rank += 1
        song = i["track"].get("track_name")
        artist = i["track"].get("artist_name")

        info.append([rank, song, artist])

    cache.set(cache_key, info, 86400)
    return info


def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    return response.json().get('access_token')


def get_album_cover(client_id, client_secret, album_name, artist_name):
    cache_key = f"cover_{album_name}_{artist_name}"
    cover_url = cache.get(cache_key)

    # 如果缓存中已经有了封面URL，直接返回该URL
    if cover_url:
        return cover_url

    # 如果没有，向Spotify API请求数据
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
                image_url = images[1].get('url') if len(images) > 1 else images[0].get('url')
                cache.set(cache_key, image_url, timeout=86400)
                return image_url
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
