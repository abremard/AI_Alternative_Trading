""" Python motley fool scraping job
"""

import time

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = parent.parent.parent
import sys
sys.path.insert(0, srcPath)

from scrape import motleyfool as mfool

# start = time.time()
# mfool.job()
# end = time.time()
# print("Earning calls extraction took a total of "+str(end - start)+" seconds")
