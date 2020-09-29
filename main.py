#!/usr/bin/python3
__author__ = "u/wontfixit"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.0"

import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from DBhelper import *
from datetime import datetime
import configparser
import logging as log

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp - (24 * 60 * 60)

LOG_FILENAME = "./log_main.log"

___debug___ = True
___runprod___ = True

if ___debug___ == True:
    log.basicConfig(handlers=[
        log.FileHandler(LOG_FILENAME),
        log.StreamHandler()], level=log.INFO, format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')


class skipr:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.client_id = config['DEFAULT']['client_id']
        self.client_secret = config['DEFAULT']['client_secret']

        self.user = None
        self.id_user = None
        self.name_user = None
        self.name_track = None
        self.id_artist = None
        self.name_artist = None
        self.id_user = None
        self.id_track = None
        self.db = None

        scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri='https://example.com'))

    def getDatabase(self, db):
        # get Database obj and pass it
        self.db = db
        return db

    def addNewIgnore(self):
        # add the current artist to ignore
        # user input must be done as well
        None

    def updateIgnore(self):
        # remove artist from ignore list
        None

    def getIgnoredArtistsByUser(self):
        return db.getArtistByUser(self.id_user, self.id_artist)

    def getCurrentPlayingTrack(self):
        res = self.sp.current_user_playing_track()
        if res is not None:
            self.name_track = res["item"]["name"]
            self.id_track = res["item"]["id"]
            artists = res["item"]["artists"]

            for artist in artists:
                self.name_artist = artist["name"]
                self.id_artist = artist["id"]
                if self.getIgnoredArtistsByUser() is True:
                    self.nextTrack()
        else:
            log.info("No running Track for {}".format(self.user["display_name"]))

    def getCurrentUserData(self):
        self.user = self.sp.current_user()
        self.id_user = self.user["id"]
        self.name_user = self.user["display_name"]

    def nextTrack(self):
        self.sp.next_track(device_id=None)
        log.info("Track skipped User: {} - Artist: {}".format(self.user["display_name"], self.name_artist))


##############################################################################################################
if __name__ == "__main__":

    skiprobj = skipr()
    db = DBhelper()
    skiprobj.getDatabase(db)

    skiprobj.getCurrentUserData()
    while True:
        skiprobj.getCurrentPlayingTrack()
        time.sleep(5)
