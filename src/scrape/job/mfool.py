import time

from scrape import motleyfool as mfool

start = time.time()
mfool.job()
end = time.time()
print("Earning calls extraction took a total of "+str(end - start)+" seconds")
