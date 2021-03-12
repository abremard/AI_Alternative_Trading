"""
Stocktwits API wrapper. Stocktwits is the largest social network for investors and traders, with over five million community members and millions of monthly visitors. StockTwits was founded in 2008, with a mission to connect regular investors and traders with each other so they can profit, learn, and have fun. For more information please refer to: https://api.stocktwits.com/developers/docs/api
"""

import requests
import json
import time

from utils import logger, request
from elk import ingest

import config

# Elastic search index
elasticPath = config.stwitsConfig["elasticPath"]

def get_stream(symbol, params=""):
    """ Returns 30 messages given a range (default to the 30 most recent messages) for the specified symbol so we need to run multiple requests by setting max value down to the oldest message in the 30 messages (given by the cursor), for example with max=298005055 for AAPL, next max is 297989058

    Args:
        symbol (str): stock or crypto symbol, example 'AAPL'
        params (str, optional): url parameters string containing max value. Defaults to "".

    Returns:
        JSON Object: Stocktwits API cursor object containing max value
    """    

    url = "https://api.stocktwits.com/api/2/streams/symbol/ric/"+symbol+".json"+params
    response, logInfo = request.get(url=url, timeout=120)
    if response.status_code == 200:
        if params != "":
            logger.debug(logInfo+' - max value is '+params.split("=")[1]+' - SUCCESS!')
        responseDict = json.loads(response.content)
        cursor = responseDict["cursor"]
        messages = responseDict["messages"]
        for message in messages:
            # Ingest into Elastic Search
            ingest.ingest(post_url=elasticPath, payload=message)
    elif response.status_code == 429:
        time.sleep(600)
        logger.error(logInfo+' - FAILED with error code '+str(response.status_code)+' and message '+response.text)
        logger.info("Skipping symbol "+symbol+" with max value "+params.split("=")[1]+" because request failed...")    
    else:
        logger.error(logInfo+' - FAILED with error code '+str(response.status_code)+' and message '+response.text)
        logger.info("Skipping symbol "+symbol+" with max value "+params.split("=")[1]+" because request failed...")
    return cursor

def extract(symbol, nb = 10, params=None):
    """ Extract stocktwits about a symbol given number of requests to perform. Each request returns only 30 stocktwits and each IP address is limited to 200 requests per hour

    Args:
        symbol (str): stock or crypto symbol
        nb (int, optional): number or requests to run. Defaults to 10.
        params (str, optional): url parameters string containing max value. Useful when user wants to scrape from where he/she left off. Defaults to None.
    """
    if params is None:
        cursor = get_stream(symbol=symbol)
    else:
        cursor = {}
        cursor["max"] = params
    for i in range(nb):
        next = cursor["max"]
        params = "?max="+str(next)
        try:
            cursor = get_stream(symbol=symbol, params=params)
        except:
            logger.info("Skipping symbol "+symbol+" because request failed...")
    return next