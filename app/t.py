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
import logging as log2
from flask import Flask, render_template, request
from flask_restful import abort
import threading


#TODO read artist which are flagged from "play less" function

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp - (24 * 60 * 60)

LOG_FILENAME = "../log_main.log"

___debug___ = True
___runprod___ = True

if ___debug___ == True:
    log2.basicConfig(handlers=[
        log2.FileHandler(LOG_FILENAME),
        log2.StreamHandler()], level=log2.INFO, format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')

class threadClass:

    def __init__(self):
        # Start the execution
        config = configparser.ConfigParser()
        config.read('config.ini')


        self.client_id = config['DEFAULT']['client_id']
        self.client_secret = config['DEFAULT']['client_secret']


        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()



    def run(self):

         #
         # This might take several minutes to complete
         while True:
            print("a")
            time.sleep(5)




app = Flask(__name__)

def test():
    print("here!")

@app.route('/', methods=["GET", "POST"])
def main():
    try:
        begin = threadClass()
    except Exception as err:
        print(str(err))
        #abort(500)

    return "Task is in progress"

def main():
    """
    Main entry point into program execution

    PARAMETERS: none
    """
    app.run(host='127.0.0.1',port=8081,threaded=True,debug=True)

##############################################################################################################
if __name__ == "__main__":
    main()