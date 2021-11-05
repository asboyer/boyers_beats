import os, json, spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id, client_secret

bad_data = ['available_markets', 'album_type', 'album_group', 'type', 
            'external_urls', 'external_ids', 'copyrights', 'label', 
            'release_date_precision', 'href', 'genres', 'is_local', 
            'disc_number', 'offset', 'limit', 'next', 'previous', 'total',
            'href', 'preview_url', "bars", "beats", "sections",
            "segments", "tatums", "meta", "followers", "popularity", "images", "id"]

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist = "Kanye West"
track_name = "Last Call"

def clean(q):
    q = q[0]
    for data_key in list(q):
        if data_key in bad_data:
            del q[data_key]
    for a in q:
        artist_list = []
        for art in a['artists']:
            artist_list.append({"name": art['name'], "uri": art["uri"]})
        a["artists"] = artist_list
    return q

tracks = clean(sp.search(q=f"artist:{artist} track:{track_name}", type='track')['tracks']['items'])

with open(f"test.json", "w") as file:
    json.dump(tracks, file, indent=4)