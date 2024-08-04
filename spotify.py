import os
import json
from flask import Flask, request, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import sys

sys.path.append("NicheRank/algo_src")

import NicheRank.algo_src.control as ctrl 
from NicheRank.algo_src.analyze_history import User_Metrics

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '52500f70b3534d0bae16a8efac5a70af'
client_secret = '42de3627a2d14129a605b2472cefbfc3'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-read-recently-played'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_recently_played'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_recently_played'))

@app.route('/get_recently_played')
def get_recently_played():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    data = sp.current_user_recently_played()
    #gets song names with url
    #song_names_info = [(item['track']['name'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_names_info])

    #gets uris with urls
    #song_uri = [(item['track']['uri'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_uri])

    #gets only uris in a list, not formatted
    
    metrics = ctrl.get_metrics_spotify_user(data)
    metrics_name = "current_metrics.json"
    save_metrics_into_json(metrics, metrics_name)

    """
    file_path = "user_history.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    """

    redirect_uri = 'http://127.0.0.1:8000/Score'
    return redirect(redirect_uri)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)



"""
client_id = '52500f70b3534d0bae16a8efac5a70af'
client_secret = '42de3627a2d14129a605b2472cefbfc3'
redirect_uri = 'http://localhost:5000/callback' # change this to website url
scope = 'user-read-recently-played'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_recently_played'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    print("in the /callback")
    return redirect(url_for('get_recently_played'))

@app.route('/get_recently_played')
def get_recently_played():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        print('hello')
        return redirect(auth_url)
    
    data = sp.current_user_recently_played()
    #gets song names with url
    #song_names_info = [(item['track']['name'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_names_info])

    #gets uris with urls
    #song_uri = [(item['track']['uri'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_uri])

    #gets only uris in a list, not formatted
    song_uris = [item['track']['uri'] for item in data.get('items', [])]
    print(song_uris)

    return song_uris
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') # redirect to home page

if __name__ == '__main__':
    app.run(debug=True)
"""

"""
THIS IS A PREVIOUS COPY - NEED SO THAT I CAN RETURN THE SONG URIS
import os
from flask import Flask, request, redirect, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

# https://developer.spotify.com/documentation/web-api/concepts/quota-modes
# add user to dev board if you want to use their account (hopefully this works)

# https://www.youtube.com/watch?v=2if5xSaZJlg&list=PL1TBkFFBtagorhLzvm5dCA1cOqJKxnWNz
# https://spotipy.readthedocs.io/en/2.16.1/
# https://developer.spotify.com/documentation/web-api/concepts/apps
# https://stackoverflow.com/questions/67264163/spotipy-exception-raised-status-403-reason-none
# https://community.spotify.com/t5/Spotify-for-Developers/Insufficient-Client-Scope-after-Refresh-Token/td-p/5526728 incorrect scope
# https://developer.spotify.com/documentation/web-api/concepts/scopes the scopes

# debugging errors

# to run this, go to terminal, run ".\venv\Scripts\activate" then "python main.py"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '52500f70b3534d0bae16a8efac5a70af'
client_secret = '42de3627a2d14129a605b2472cefbfc3'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-read-recently-played'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_recently_played'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_recently_played'))


@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])

    return playlists_html

@app.route('/get_recently_played')
def get_recently_played():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    data = sp.current_user_recently_played()
    #gets song names with url
    #song_names_info = [(item['track']['name'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_names_info])

    #gets uris with urls
    #song_uri = [(item['track']['uri'], item['track'].get('external_urls', {}).get('spotify', '')) for item in data.get('items', [])]
    #song_names_html = '<br>'.join([f'{name}: <a href="{url}">{url}</a>' if url else name for name, url in song_uri])

    #gets only uris in a list, not formatted
    song_uris = [item['track']['uri'] for item in data.get('items', [])]
    
    return song_uris

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)
"""