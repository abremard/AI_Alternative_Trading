""" Python coindesk scraping job
"""

import time

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = parent.parent.parent
import sys
sys.path.insert(0, srcPath)

from scrape import coindesk

# start = time.time()
# coindesk.job()
# end = time.time()
# print("Crypto news extraction took a total of "+str(end - start)+" seconds")