import os
import sys
import json
from flask import Flask, request, redirect, session, url_for, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from flask_cors import CORS

sys.path.append("NicheRank/algo_src")

import control as ctrl
from analyze_history import User_Metrics

#this is how to start the file with Flask, then create a randomized secret key
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(64)


#this is connecting the Spotify for Developers (SfD) with my project- the client ID and Secret are what connects them
client_id = '52500f70b3534d0bae16a8efac5a70af'
client_secret = '42de3627a2d14129a605b2472cefbfc3'
#this redirect uri is authorized within the SfD, and is used within the auth_url (very important!!)
redirect_uri = 'http://localhost:5000/callback'
#this is what determines what displays when I am asking for user permission for their data
scope = 'user-read-recently-played'

#CHANGE THIS OPTION FOR DIFFERENT USERS.
# 0 is spotify login. (spotify accounts need to be authenticated in SfD) login with user: Amanda Brannon pw: Workingonit1!
# 1,2,3 are differently generated users with 100000 points of data
user_option = 0

#this makes a new session upon opening the page- this is important as the authorization token is only temporary
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


#this is the landing page. it checks whether you have logged in yet. if you have (you probably haven't) it goes straight to collecting
#data and automatically rerouting you to your score page. It HAS to redirect to auth_url, or else you will get stuck in a deadlock.
#that auth_url contains the client id and redirect_uri and looks like 
#this: https://accounts.spotify.com/authorize?client_id=52500f70b3534d0bae16a8efac5a70af&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback&scope=user-read-recently-played&show_dialog=True
@app.route('/')
def home():
    if (user_option == 0):
        if not sp_oauth.validate_token(cache_handler.get_cached_token()):
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)
        return redirect(url_for('get_recently_played'))
    elif (user_option == 1):
        return redirect(url_for('fake_user1'))
    elif (user_option == 2):
        return redirect(url_for('fake_user2'))
    elif (user_option == 3):
        return redirect(url_for('fake_user3'))


#this callback function happens when you have logged in- it authorizes with your access token and reroutes you to collecting data
#and going to the score page
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_recently_played'))


#this happens so fast you never see the page! this checks again to make sure you are authorized. It then takes the 50 most recently
#played songs and puts them in a .json file to be taken in by another file for analysis. the redirectUri is manually changed
#so that you can get to your score page (this redirect connection point took us hours to figure out.)
@app.route('/get_recently_played')
def get_recently_played():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    data = sp.current_user_recently_played()
    
    file_path = "user_history.json"
    with open(file_path, "w") as f:
        json.dump(data, f)

    #return redirect(url_for('fake_user1'))
    redirect_uri = 'http://127.0.0.1:8000/Score'
    return redirect(redirect_uri)

@app.route('/user_metrics', methods=['GET'])   #http://127.0.0.1:5000/user_metrics
def user_metrics():
    sorting_type = "q"  # can be q or m
    history_path = "user_history.json"
    metrics: User_Metrics = ctrl.get_metrics_spotify_user(history=history_path, sorting_type=sorting_type)

    # Access the favorites attribute directly from the Artist_Metrics
    artist_list = metrics.artist_metrics.favorites

    #Access song metrics
    song_list = metrics.song_metrics.favorites
    #print(song_list[:10])

    # Access the pop_score attribute
    pop_score = metrics.pop_score


    # Create a response dictionary containing both the artist list and the pop score
    response = {
        "topArtists": artist_list[:10],  # get only the top 10 favorite artists
        "pop_score": pop_score,
        "topSongs": song_list[:10]
    }

    return jsonify(response)

@app.route('/fake_user1', methods=['GET'])   #http://127.0.0.1:5000/fake_user1
def fake_user1():
    fake_metrics: User_Metrics= ctrl.get_metrics_fake_user(history_size=100000, pop_level="med", gen_type="greedy", sorting_type="q")
    return jsonify(fake_metrics)

@app.route('/fake_user2', methods=['GET'])   #http://127.0.0.1:5000/fake_user2
def fake_user2():
    fake_metrics: User_Metrics= ctrl.get_metrics_fake_user(history_size=100000, pop_level="low", gen_type="greedy", sorting_type="m")
    return jsonify(fake_metrics)

@app.route('/fake_user3', methods=['GET'])   #http://127.0.0.1:5000/fake_user3
def fake_user3():
    fake_metrics: User_Metrics= ctrl.get_metrics_fake_user(history_size=100000, pop_level="high", gen_type="greedy", sorting_type="q")
    return jsonify(fake_metrics)

#this never happens since we redirect to the frontend :)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url)

#the backbone of all python files
if __name__ == '__main__':
    app.run(debug=True)