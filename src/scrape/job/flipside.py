""" Python flipside scraping job
"""

import time

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = parent.parent.parent
import sys
sys.path.insert(0, srcPath)

from scrape import flipside

if __name__ == "__main__":
    start = time.time()
    flipside.job(projects=["BTC", "ETH", "LTC", "XRP", "USDT", "UNI", 'LINK', "ADA", "DOT", "XLM", "BNB", "TRX"])
    end = time.time()
    print("Crypto ratings extraction took a total of "+str(end - start)+" seconds")