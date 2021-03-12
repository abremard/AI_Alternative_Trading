"""
Backed by the prestigious Y Combinator and composed of a tight-knit community of researchers, engineers, and business professionals, Alpha Vantage Inc. has partnered with major exchanges and institutions around the world to become a leading provider of stock APIs as well as forex (FX) and digital/crypto currency data feeds. Our stock market API design philosophy is centered around rigorous research, cutting edge technology, and an unwavering focus on democratizing access to financial data.
"""

import urllib
import json
import time

from utils import logger, request
from elk import ingest

def api_req(params):
    """ Alpha vantage API wrapper. For more information please refer to: https://www.alphavantage.co/documentation/

    Args:
        params (dict): Python dict request parameters

    Returns:
        requests.Response Object 
    """    

    # Sleeps for 12 seconds because API allows 5 requests per minute
    time.sleep(12)
    # Prepare request
    baseUrl = "https://www.alphavantage.co/query?"
    params["apikey"] = "M1V7YKMWNYU2J3NC"
    paramString = urllib.parse.urlencode(params)
    finalUrl = baseUrl + paramString
    # Send request
    response, logInfo = request.get(url=finalUrl, timeout=120)
    # Log response
    if response.status_code == 200:
        logger.debug(logInfo+' - SUCCESS!')
    else:
        logger.error(logInfo+' - FAILED with error code '+str(response.status_code)+' and message '+response.text)
    return response


def daily_download(symbols):
    """ This API endpoints returns raw (as-traded) daily open/high/low/close/volume values, daily adjusted close values, and historical split/dividend events of the global equity specified, covering 20+ years of historical data.

    Args:
        symbols (str[]): Array of symbols from which price data will be extracted
    """    
    # Elastic search index    
    elasticPath = "http://localhost:9200/daily_stock/ingest"
    
    for symbol in symbols:
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",
            "datatype": "json"
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            responseDict = responseDict["Time Series (Daily)"]
            # Parse JSON response
            for attr, value in responseDict.items():
                tmpDict = {}
                tmpDict["symbol"] = symbol
                tmpDict["day"] = attr
                tmpDict["open"] = value["1. open"]
                tmpDict["high"] = value["2. high"]
                tmpDict["low"] = value["3. low"]
                tmpDict["close"] = value["4. close"]
                tmpDict["adjusted_close"] = value["5. adjusted close"]
                tmpDict["volume"] = value["6. volume"]
                tmpDict["dividend_amount"] = value["7. dividend amount"]
                tmpDict["split_coefficient"] = value["8. split coefficient"]
                # Ingest into Elastic Search
                ingest.ingest(post_url=elasticPath, payload=tmpDict)            
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def income_statement_download(symbols):
    """ This API returns the annual and quarterly income statements for the company of interest. Data is generally refreshed on the same day a company reports its latest earnings and financials.

    Args:
        symbols (str[]): Array of symbols from which income statements will be extracted
    """    
    # Elastic search index
    elasticPath = "http://localhost:9200/income_statement/ingest"

    for symbol in symbols:
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            # only keep quarterly reports
            del responseDict["annualReports"]
            for report in responseDict["quarterlyReports"]:
                report["symbol"] = symbol
                # Ingest into Elastic Search
                ingest.ingest(post_url=elasticPath, payload=report)
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def balance_sheet_download(symbols):
    """ This API returns the annual and quarterly balance sheets for the company of interest. Data is generally refreshed on the same day a company reports its latest earnings and financials.

    Args:
        symbols (str[]): Array of symbols from which balance sheets will be extracted
    """    
    # Elastic search index
    elasticPath = "http://localhost:9200/balance_sheet/ingest"

    for symbol in symbols:
        params = {
            "function": "BALANCE_SHEET",
            "symbol": symbol,
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            # only keep quarterly reports
            del responseDict["annualReports"]
            for report in responseDict["quarterlyReports"]:
                report["symbol"] = symbol
                # Ingest into Elastic Search
                ingest.ingest(post_url=elasticPath, payload=report)
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def cash_flow_download(symbols):
    """ This API returns the annual and quarterly cash flows for the company of interest. Data is generally refreshed on the same day a company reports its latest earnings and financials.

    Args:
        symbols (str[]): Array of symbols from which cash flows will be extracted
    """
    # Elastic search index
    elasticPath = "http://localhost:9200/cash_flow/ingest"

    for symbol in symbols:
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            # only keep quarterly reports
            del responseDict["annualReports"]
            for report in responseDict["quarterlyReports"]:
                report["symbol"] = symbol
                # Ingest into Elastic Search
                ingest.ingest(post_url=elasticPath, payload=report)
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def earnings_download(symbols):
    """ This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics.

    Args:
        symbols (str[]): Array of symbols from which earnings will be extracted
    """    
    # Elastic search index
    elasticPath = "http://localhost:9200/earnings/ingest"    
    for symbol in symbols:
        params = {
            "function": "EARNINGS",
            "symbol": symbol,
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            del responseDict["annualEarnings"]
            for earning in responseDict["quarterlyEarnings"]:
                earning["symbol"] = symbol
                ingest.ingest(post_url=elasticPath, payload=earning)
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def crypto_daily(symbols, market="USD"):
    """ This API returns the daily historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

    Args:
        symbols (str[]): Array of symbols from which price data will be extracted
        market (str, optional): Market on which the symbol is traded. Defaults to "USD".
    """
    # Elastic search index
    elasticPath = "http://localhost:9200/daily_crypto/ingest"
    for symbol in symbols:
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": market
        }
        response = api_req(params=params)
        if response.status_code == 200:
            responseDict = json.loads(response.content)
            responseDict = responseDict["Time Series (Digital Currency Daily)"]
            for attr, value in responseDict.items():
                tmpDict = {}
                tmpDict["symbol"] = symbol
                tmpDict["day"] = attr
                tmpDict["open"] = value["1b. open (USD)"]
                tmpDict["high"] = value["2b. high (USD)"]
                tmpDict["low"] = value["3b. low (USD)"]
                tmpDict["close"] = value["4b. close (USD)"]
                tmpDict["volume"] = value["5. volume"]
                tmpDict["market_cap"] = value["6. market cap (USD)"]
                # Ingest into Elastic Search
                ingest.ingest(post_url=elasticPath, payload=tmpDict)
        else:
            logger.info("Skipping "+symbol+" because request failed...")

def job(symbols):
    """ Scrape job for stocks. Gets daily prices + SEC informations

    Args:
        symbols (str[]): list of stock symbols to extract data from
    """    
    # ------------- TIME SERIES --------------
    # daily_download(symbols=symbols)
    # ------------- SEC FILINGS --------------
    income_statement_download(symbols=symbols)
    balance_sheet_download(symbols=symbols)
    cash_flow_download(symbols=symbols)
    earnings_download(symbols=symbols)

def crypto_job(symbols):
    """ Scrape job for crypto. Gets daily prices

    Args:
        symbols (str[]): list of crypto symbols to extract data from
    """    
    crypto_daily(symbols=symbols)