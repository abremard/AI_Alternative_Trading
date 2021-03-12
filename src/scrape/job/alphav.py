""" Python alphavantage scraping job
"""

import time

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = parent.parent.parent
import sys
sys.path.insert(0, srcPath)

from scrape import alphavantage as alphav

# start = time.time()
# alphav.job(symbols=["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"])
# step = time.time()
# print("Stock extraction took a total of "+str(step - start)+" seconds")
# alphav.crypto_job(symbols=["BTC", "ETH", "LTC", "XRP"])
# end = time.time()
# print("Crypto extraction took a total of "+str(end - step)+" seconds")