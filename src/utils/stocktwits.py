import requests
from utils import logger, utils
import json

def get_stream(symbol, params=""):
    
    # the endpoint below only returns 30 results, run multiple requests by setting max value
    # down to the oldest message in the 30 messages (given by the cursor), with max=298005055, next max is 297989058
    # regulate scraping with the created_at date
    
    url = "https://api.stocktwits.com/api/2/streams/symbol/ric/"+symbol+".json"+params
    responseText, logInfo = utils.request(url=url, rtype='GET', timeout=120)
    # print(responseText.headers)
    logger.log(logInfo)
    responseDict = json.loads(responseText.content)
    symbolDict = responseDict["symbol"]
    cursor = responseDict["cursor"]
    messages = responseDict["messages"]
    for message in messages:
        del message["user"]
        del message["source"]
        del message["symbols"]
        del message["mentioned_users"]
    date = message["created_at"]
    # print(messages)
    # outputPath = "./data/stocktwits/"+symbol+"_"+str(cursor["max"])+"-"+str(cursor["since"])+".json"
    # with open(outputPath,  "w", encoding="utf8") as outf:
    #     outf.write(json.dumps(messages))
    return messages, symbolDict, cursor, date

def extract(symbol, params=None):
    # limited to 200 requests per hour, meaning 6000 messages per hour (~5 days of message)
    # 1 hour scrape for 1 week of 1 symbol
    if params is None:
        messages, symbolDict, cursor, date = get_stream(symbol=symbol)
        messagesList = messages
    else:
        cursor = {}
        cursor["max"] = params
        messagesList = []
    for i in range(199):
        next = cursor["max"]
        params = "?max="+str(next)
        messages, symbolDict, cursor, date = get_stream(symbol=symbol, params=params)
        print(date, next)
        messagesList = messagesList + messages
    outputPath = "./data/stocktwits/"+str(i+2)+"-"+symbol+"_"+str(next)+".json"
    with open(outputPath, "w", encoding="utf8") as outf:
        outf.write(json.dumps(messagesList))
    outputPath = "./data/stocktwits/"+symbol+"-metadata.json"
    with open(outputPath, "w", encoding="utf8") as outf:
        outf.write(json.dumps(symbolDict))
