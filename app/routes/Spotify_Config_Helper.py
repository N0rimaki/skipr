import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from DBhelper import *



class Spotify_Config_Helper:
    def __init__(self):
        config = configparser.ConfigParser()
        #config.read('../../config.ini')
        config.read('config.ini')

        self.SPOTIPY_CLIENT_ID = config['SPOTIFY']['SPOTIPY_CLIENT_ID']
        self.SPOTIPY_CLIENT_SECRET = config['SPOTIFY']['SPOTIPY_CLIENT_SECRET']
        self.SPOTIPY_REDIRECT_URI = config['SPOTIFY']['SPOTIPY_REDIRECT_URI']


class skipr():
    def __init__(self,spotify):
       # Spotify_Config_Helper.__init__(self)

        self.user = None
        self.id_user = None
        self.name_user = None
        self.name_track = None
        self.id_artist = None
        self.name_artist = None
        self.id_user = None
        self.id_track = None
        self.db = None
        self.spotify = spotify
        self.IsIgnoredArtistsByUser = False

        #scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
        #self.sp = spotipy.Spotify(auth_manager=authstuff)

    def get_token(self,token):
        # not used anymore... but how then?
       # sp = spotipy.SpotifyOAuth.get_access_token(token,as_dict=False,check_cache=False)
        return False

    def getDatabase(self, db):
        # get Database obj and pass it
        self.db = db
        return db

    def addNewIgnore(self,arg_name_artist):
        # add the current artist to ignore
        # user input must be done as well
        self.getCurrentUserData()
       # self.getDatabase(self.db.addNewIgnore(self.id_user, self.name_user, None, arg_name_artist))

        print(self.sp.search(q=arg_name_artist, limit=10, type="artist"))

    def addNewUserToken(self,a,b,token):
        #self.getCurrentUserData(self)
        #self.getDatabase(self.db.addNewUser(self.id_user, self.name_user, token))
        self.getDatabase(self.db.addNewUser(a, b, token))


    def updateIgnore(self):
        # remove artist from ignore list
        None

    def getIgnoredArtistsByUser(self):
        self.IsIgnoredArtistsByUser = self.getDatabase(self.db.getArtistByUser(self.id_user, self.id_artist, self.name_artist))


    def getCurrentPlayingTrack(self):

        # track = spotify.current_user_playing_track()
        # if not track is None:
        #    return track
        # return "No track currently playing."
        track = self.spotify.current_user_playing_track()
        #log.info("{}".format(res))
        if not track is None:
            self.name_track = track["item"]["name"]
            self.id_track = track["item"]["id"]
            artists = track["item"]["artists"]

            for artist in artists:
                self.name_artist = artist["name"]
                self.id_artist = artist["id"]
                self.getIgnoredArtistsByUser()
                if self.IsIgnoredArtistsByUser is True:
                    self.nextTrack()

        return  "No track currently playing."

    def getCurrentUserData(self):
        self.user = self.spotify.current_user()
        self.id_user = self.user["id"]
        self.name_user = self.spotify.me()["display_name"]
        self.user_pp_url = self.user["images"][0]["url"]


    def nextTrack(self):
        self.spotify.next_track(device_id=None)
       # log.info("Track skipped User: {} - Artist: {}".format(self.user["display_name"], self.name_artist))