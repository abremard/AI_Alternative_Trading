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


# ----------------------------------------------------------------------------------------------------------------
# -------- MAIN ---------
# parameters
symbols = ["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"]
# script
logger.log_config()
# alphav.daily_download(symbols=symbols)
# alphav.income_statement_download(symbols)
# alphav.balance_sheet_download(symbols)