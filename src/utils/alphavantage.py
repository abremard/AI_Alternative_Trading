import os
import subprocess
import datetime
import logging
import urllib
import sys
import pandas as pd
import io

from utils import logger, utils

def api_req(params, format, outputPath):
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
        rawData.to_csv(outputPath, index=False)
    elif format == "json":
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
        outputPath = "./data/time-series/"+symbol+".csv"
        api_req(params=params, format="csv", outputPath=outputPath)

def income_statement_download(symbols):
    for symbol in symbols:
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
        }
        outputPath = "./data/fundamental/income-statement/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)

def balance_sheet_download(symbols):
    for symbol in symbols:
        params = {
            "function": "BALANCE_SHEET",
            "symbol": symbol,
        }
        outputPath = "./data/fundamental/balance-sheet/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)

def cash_flow_download(symbols):
    for symbol in symbols:
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
        }
        outputPath = "./data/fundamental/cash-flow/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)

def earnings_download(symbols):
    for symbol in symbols:
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
        }
        outputPath = "./data/fundamental/earnings/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)

def crypto_daily(symbols, market="USD"):
    for symbol in symbols:
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": market
        }
        outputPath = "./data/crypto/daily/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)

def crypto_rating(symbols):
    # This is for real-time data, for historical data use flipside API wrapper instead
    for symbol in symbols:
        params = {
            "function": "CRYPTO_RATING",
            "symbol": symbol,
        }
        outputPath = "./data/crypto/rating/"+symbol+".json"
        api_req(params=params, format="json", outputPath=outputPath)