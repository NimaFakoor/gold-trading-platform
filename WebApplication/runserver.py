__author__ = "NimaFakoor"
__version__ = '1.0.0'

"""
This script runs the web application using a development server.
"""

from os import environ
import logging
from WebApplication import app

if __name__ == '__main__':

    HOST = environ.get('SERVER_HOST', 'localhost')
    #logging.basicConfig(filename='serverlog.log',format='[%(funcName)s] - %(levelname)s [%(asctime)s] %(message)s' , level=logging.DEBUG) 

    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
