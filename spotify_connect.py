import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
from configparser import ConfigParser


config = ConfigParser()
config.read('notes/config.ini')
sp_token = config.get('spotify', 'client_id')
sp_secret = config.get('spotify', 'client_secret')
sp_uri = config.get('spotify', 'redirect_uri')
# from server import get_data_from_html

os.environ['SPOTIPY_CLIENT_ID'] = sp_token
os.environ['SPOTIPY_CLIENT_SECRET'] = sp_secret
os.environ['SPOTIPY_REDIRECT_URI'] = sp_uri


ask = input("Enter the date which you want to go to (YYYY-MM-DD):- ")
# ask = get_data_from_html()
NUMBER_OF_SONGS = 10
# response = requests.get("https://www.billboard.com/charts/india-songs-hotw/"+ask)
response = requests.get("https://www.billboard.com/charts/hot-100/" + ask)
soup = BeautifulSoup(response.text, "html.parser")
# print(soup)
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
song_names = song_names[:NUMBER_OF_SONGS]

# print(song_names)
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Authentication - without user
# client_credentials_manager = SpotifyClientCredentials(client_id=sp_token, client_secret=sp_secret)
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=sp_token,
                                                    client_secret=sp_secret,
                                                    redirect_uri='https://localhost:8000/callback'))

print(spotify)
user_id = spotify.me()["id"]
song_uris = {}
year = ask.split("-")[0]

for song in song_names:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        name = result['tracks']['items'][0]['name']
        song_uris[uri] = name
    except IndexError:
        print(f"{song} doesn't exist in Spotify. SKIPPED.")
# print(song_uris)

# new_playlist = spotify.user_playlist_create(user=user_id, name=f"{ask} Billboard 20", public=False,
#                                             description=f"Here are the top 20 songs which featured on Billboard on "
#                                                         f"{ask}.")
#
# spotify.playlist_add_items(playlist_id=new_playlist['id'], items=song_uris)

# http://open.spotify.com/track/   s=spotify:track:3G6hxSp260RzGw4sOiDOQ3 s[14:]

song_urls = {}
url_start = "https://open.spotify.com/track/"
for song in song_uris.keys():
    key = url_start + song[14:]
    val = song_uris[song]
    song_urls[key] = val
# print(song_urls)
