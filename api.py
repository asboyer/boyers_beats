import os, json, spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id, client_secret

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def clean(q):
    if q == []:
        return q
    q = q[0]
    artist_list = []
    for art in q['artists']:
        artist_list.append({"name": art['name'], "uri": art["uri"]})
    q["artists"] = artist_list
    return q

def get_uri(track_name, artist):
    tracks = clean(sp.search(q=f"artist:{artist} track:{track_name}", type='track')['tracks']['items'])
    if tracks == []:
        return '', ''
    else:
        return tracks['uri'], tracks['album']['uri']

def get_img(album_uri):
    result = sp.album(album_uri)
    best_image_url = ''
    for image in result['images']:
        if image['height'] == 640:
            return image['url']