import os
from flask import render_template, Blueprint, request, redirect, url_for, session

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.routes.Spotify_Config_Helper import Spotify_Config_Helper,skipr
import uuid
from DBhelper import *


spothelp = Spotify_Config_Helper()

SPOTIPY_CLIENT_ID = spothelp.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = spothelp.SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI = spothelp.SPOTIPY_REDIRECT_URI

os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI


caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    session_tmp = caches_folder + session.get('uuid')
    print(str(session_tmp))
    return session_tmp

blueprint = Blueprint('app', __name__)


@blueprint.route("/login", methods=['POST', 'GET'])
def login():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope, cache_path=session_cache_path(),show_dialog=True)

    return redirect(auth_manager.get_authorize_url())


@blueprint.route("/callback")
def callback():
    # Requests refresh and access tokens
    auth_token = request.args.get('code')

    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path()
                                               ,client_id=SPOTIPY_CLIENT_ID,
                                                          client_secret=SPOTIPY_CLIENT_SECRET,
                                                        redirect_uri=SPOTIPY_REDIRECT_URI)

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    skiprobj = skipr(spotify)
    db = DBhelper()
    skiprobj.getDatabase(db)
    skiprobj.addNewUserToken("a","b","c")

    if request.args.get("code"):

    #   Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/me')

    if not auth_manager.get_cached_token():
        print("NO Cached TOKEN")
     # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_manager.get_authorize_url())


    return redirect(url_for("app.me"))


@blueprint.route("/me")
def me():
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=session_cache_path())
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    skiprobj = skipr(spotify)
    db = DBhelper()
    skiprobj.getDatabase(db)

    skiprobj.getCurrentUserData()
    skiprobj.getCurrentPlayingTrack()
    var = skiprobj.name_user
    tr = skiprobj.name_track
    at = skiprobj.name_artist
    print(at)
    return render_template("me.html",name_of_me=var,track_playing=tr,user_pp_url=skiprobj.user_pp_url)

@blueprint.route("/")
def main():
    return render_template('main.html')

@blueprint.route("/not-found")
def not_found():
    return render_template('404.html')


@blueprint.route("/load", methods=['GET', 'POST'])
def load():
    authorization_header = session['authorization_header']
    extract_letters = lambda x: ''.join([letter for letter in x if not letter.isdigit()])

    if request.method == 'GET':
        # -------- Get user's name, id, and set session --------
        profile_data = spotify_handler.get_user_profile_data(authorization_header)
        user_display_name, user_id = profile_data['display_name'], profile_data['id']
        session['user_id'], session['user_display_name'] = user_id, user_display_name

        # -------- Get user playlist data --------
        playlist_data = spotify_handler.get_user_playlist_data(authorization_header, user_id)

        return render_template('select.html',
                               user_display_name=user_display_name,
                               playlists_data=playlist_data,
                               func=extract_letters)

    return render_template('404.html')




