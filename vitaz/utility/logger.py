import logging
from datetime import datetime


def saveMsg(msg):
    logging.info(msg)


logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s: %(message)s',
    datefmt='[%d/%m/%y][%H:%M:%S]'
    )
