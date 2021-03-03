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

# ----------------------------------------------------------------------------------------------------------------
# -------- MAIN ---------
# parameters
# symbols = ["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"]
symbols = ["IBM"]
# script
logger.log_config()
# mfool.all_transcripts_download(startPage=3,endPage=4)
alphav.daily_download(symbols=symbols)
alphav.income_statement_download(symbols)
# alphav.balance_sheet_download(symbols)