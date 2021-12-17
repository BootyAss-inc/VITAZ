import logging
from datetime import datetime


def saveInfo(msg):
    logging.basicConfig(filename='log.log', level=logging.INFO)
    date = datetime.now().strftime(' [%H:%M:%S]: ')
    logging.info(date + msg)


def saveError(msg):
    logging.basicConfig(filename='log.log', level=logging.ERROR)
    date = datetime.now().strftime('[%H:%M:%S]: ')
    logging.error(date + msg)
