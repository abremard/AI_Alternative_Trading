""" Python alphavantage scraping job
"""

import time

import sys
sys.path.insert(0,"C:\\Users\\Alexandre\\Documents\\Projects\\Trading\\AI_Alternative_Trading\\src")

from scrape import alphavantage as alphav

# start = time.time()
# alphav.job(symbols=["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"])
# step = time.time()
# print("Stock extraction took a total of "+str(step - start)+" seconds")
# alphav.crypto_job(symbols=["BTC", "ETH", "LTC", "XRP"])
# end = time.time()
# print("Crypto extraction took a total of "+str(end - step)+" seconds")