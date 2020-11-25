#!/usr/bin/python3
__author__ = "u/wontfixit"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.0"

import configparser
import time

from flask import Flask, render_template, request
from flask_restful import abort
import threading
from flask_executor import Executor

app = Flask(__name__)

executor = Executor(app)

@app.route('/', methods=["GET", "POST"])
def test():
   # executor.submit(loop)
    loop.submit()
    if request.method == "POST":
        print("kk")
    return render_template("page.html", mytitle="pagetitle")


def main():
    """
    Main entry point into program execution

    PARAMETERS: none
    """
    try:
        app.run(debug=True, host="127.0.0.1", port=8081)
    except Exception as err:
        print("{}".format(err))


##############################################################################################################
if __name__ == "__main__":
    main()
