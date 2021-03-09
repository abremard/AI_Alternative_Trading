import time

from scrape import coindesk

start = time.time()
coindesk.job()
end = time.time()
print("Crypto news extraction took a total of "+str(end - start)+" seconds")