import logging
import os

class Logs:
    LEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    FORMAT = '%(asctime)s [%(levelname)5s] %(filename)s :: %(funcName)s() - %(message)s'
