from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests as re
import qrcode
import pymongo
import gridfs

app = Flask(__name__)
NUMBER_OF_SONGS = 10


@app.route('/', methods=['GET'])
def show_home():
    return render_template('home.html')


@app.route('/send_data', methods=['POST', 'GET'])
def get_data_from_html():
    if request.method == 'POST':
        form = request.form
        print(form)
        date = form['Date']
        print(date)

        response = re.get("https://www.billboard.com/charts/hot-100/" + date)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup)
        song_names_spans = soup.select("li ul li h3")
        song_names = [song.getText().strip() for song in song_names_spans]
        song_names = song_names[:NUMBER_OF_SONGS]

        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='35514d70c0c24cf59b6c9f44cb988fee',
                                                            client_secret='1be99c3df1564884bceb33c8554c42fb',
                                                            redirect_uri='https://localhost:8000/callback'))

        user_id = spotify.current_user()["id"]
        song_uris = {}
        year = date.split("-")[0]

        for song in song_names:
            result = spotify.search(q=f"track:{song} year:{year}", type="track")
            # print(result)
            try:
                uri = result['tracks']['items'][0]['uri']
                name = result['tracks']['items'][0]['name']
                song_uris[uri] = name
            except IndexError:
                print(f"{song} doesn't exist in Spotify. SKIPPED.")

        song_urls = {}
        url_start = "https://open.spotify.com/track/"
        for song in song_uris.keys():
            key = url_start + song[14:]
            val = song_uris[song]
            song_urls[key] = val
        # print(song_urls)

        with open("songs.txt", "w") as f:
            f.write(f"WELCOME TO THE SPOTIFY {date} PLAYLIST\n")
            for key, val in song_urls.items():
                f.write('%s : %s\n' % (key, val))

        with open("songs.txt", "r") as f:
            data = f.read()

        img = qrcode.make(data)
        img.save('songs_qr.jpg')

        return song_urls


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
