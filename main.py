#!/usr/bin/python3
__author__ = "u/wontfixit"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.0"

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json

import re
from datetime import datetime
import configparser
import logging as log

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp-(24*60*60)

LOG_FILENAME = "./log_main.log"


___debug___ = True
___runprod___= True

if ___debug___ == True:
		log.basicConfig( handlers=[
            log.FileHandler(LOG_FILENAME),
            log.StreamHandler()],level=log.INFO,format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')



class skipr:
    def init(self):
        None



if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    client_id = config['DEFAULT']['client_id']
    client_secret = config['DEFAULT']['client_secret']

    scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=client_id,
                                                               client_secret=client_secret,redirect_uri='https://example.com'))



    user = sp.current_user()
    res = sp.current_user_playing_track()
    print(res)
   # js = json.loads(res)

    namelist = res["item"]["artists"]
    for artist in namelist:
     print(artist["name"]+" "+artist["id"])
     if artist["id"] == "7gHscNMDI8FF8pcgrV8eIn":
         next = sp.next_track(device_id=None)


    track = res["item"]["name"]
    track_id = res["item"]["id"]

   # print(str(name))
    print(str(track))
    print(str(track_id))

    #next = sp.next_track(device_id=None)