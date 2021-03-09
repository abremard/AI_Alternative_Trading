import time

from scrape import flipside

start = time.time()
flipside.job(projects=["BTC", "ETH", "LTC", "XRP", "USDT", "UNI", 'LINK', "ADA", "DOT", "XLM", "BNB", "TRX"])
end = time.time()
print("Crypto ratings extraction took a total of "+str(end - start)+" seconds")