""" Python alphavantage scraping job
"""

import time

from scrape import alphavantage as alphav

start = time.time()
alphav.job(symbols=["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"])
step = time.time()
print("Stock extraction took a total of "+str(step - start)+" seconds")
alphav.crypto_job(symbols=["BTC", "ETH", "LTC", "XRP", "USDT", "UNI", 'LINK', "ADA", "DOT", "XLM", "BNB", "TRX"])
end = time.time()
print("Crypto extraction took a total of "+str(end - step)+" seconds")