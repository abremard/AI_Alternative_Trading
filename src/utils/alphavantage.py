from utils import utils
import os
import subprocess
import datetime
import logging
import urllib
import sys
import pandas as pd
import io

from utils import logger, utils

def api_req(params, format):
    """ Alpha vantage API wrapper. For more information please refer to: https://www.alphavantage.co/documentation/
    """
    baseUrl = "https://www.alphavantage.co/query?"
    params["apikey"] = "M1V7YKMWNYU2J3NC"
    paramString = urllib.parse.urlencode(params)
    finalUrl = baseUrl + paramString
    responseText, logInfo = utils.request(url=finalUrl, rtype='GET', timeout=120)
    logger.log(logInfo)
    if format == "csv":
        rawData = pd.read_csv(io.StringIO(responseText.content.decode('utf-8')))
        outputPath = "./data/"+params['symbol']+".csv"
        rawData.to_csv(outputPath, index=False)
    elif format == "json":
        outputPath = "./data/"+params['symbol']+".json"
        with open(outputPath, 'wb') as outf:
            outf.write(responseText.content)

def daily_download(symbols):
    for symbol in symbols:
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",
            "datatype": "csv"
        }
        api_req(params=params, format="csv")

def income_statement_download(symbols):
    for symbol in symbols:
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
        }
        api_req(params=params, format="json")

def balance_sheet_download(symbols):
    for symbol in symbols:
        params = {
            "function": "BALANCE_SHEET",
            "symbol": symbol,
        }
        api_req(params=params, format="json")

def cash_flow_download(symbols):
    for symbol in symbols:
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
        }
        api_req(params=params, format="json")

def earnings_download(symbols):
    for symbol in symbols:
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
        }
        api_req(params=params, format="json")