""" Python stwits scraping job
"""

import time

import config
srcPath = config.stwitsConfig['srcPath'].replace("\\", "\\\\")

import sys
sys.path.insert(0, srcPath)

from scrape import stocktwits as stwits

def job(symbol):
    """ Extraction job for given symbol. 200 requests are fired every hour, scrapes 144000 stocktwits per day.

    Args:
        symbol (str): stock or crypto symbol, for example "AAPL"
    """
    next = stwits.extract(symbol=symbol, nb=190)
    time.sleep(3660)
    while True:
        next = stwits.extract(symbol=symbol, nb=200, params=next)
        time.sleep(3660)

# start = time.time()
# job(config.stwitsConfig['symbol'])
# end = time.time()
# print("Stocktwits extraction took a total of "+str(end - start)+" seconds")