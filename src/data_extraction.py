import requests
import os
import subprocess
import datetime
import logging
import urllib
import sys
import pandas as pd
import io

from utils import logger, utils
from utils import alphavantage as alphav
from utils import motleyfool as mfool
from utils import stocktwits as stwits
from utils import flipside
from utils import coindesk

# ----------------------------------------------------------------------------------------------------------------

logger.log_config()

# ------------- EARNING CALLS --------------

# mfool.all_transcripts_download(startPage=3,endPage=4)

# ------------- TIME SERIES --------------

# symbols = ["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"]
# symbols = ["IBM"]
# alphav.daily_download(symbols=symbols)

# ------------- SEC FILINGS --------------

# alphav.income_statement_download(symbols)
# alphav.balance_sheet_download(symbols)
# alphav.cash_flow_download(symbols)
# alphav.earnings_download(symbols)

# ------------- STOCKTWITS --------------

# symbol = "BTC"
# stwits.extract(symbol=symbol, params=294481182)

# ------------- FLIPSIDE --------------

# projects = ['BTC', 'ETC', 'ETH']
# '''
# dev : A daily composite score representing the amount and type of work being done on a product. This score tracks activity across three major categories: changes to the codebase, major releases and updates, and community involvement.
# fcas : A proprietary rating derived from the activity of developers, on chain behaviors and market activity.
# market-maturity : Market Maturity, derived from Risk and Money Supply factors, represents the likelihood a crypto asset will provide consistent returns across various market scenarios by combining assessments of market risk (specifically, exchange liquidity, price projections, price cliff potential, algorithmic prediction consistency, and price volatility), as well as an analysis of the stability of the Money Supply of each tracked project. The less stable the Money Supply, and the more controlled it is by a few addresses, the worse the Money Supply score.
# utility : A distilled representation of non-exchange related economic activity. Computed daily.
# '''
# metrics = ['dev', 'fcas', 'market-maturity', 'utility']
# start_timestamp = "2019-01-01T00:00:00Z"
# end_timestamp = "2021-01-01T00:00:00Z"
# period = "day"
# flipside.metrics_download(projects=projects, metrics=metrics, start_timestamp=start_timestamp, end_timestamp=end_timestamp, period=period)

# ------------- COIN DESK --------------

coindesk.all_articles_download(symbol="btc", startPage=1, endPage=2)
