""" Python alphavantage scraping job
"""

import time

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = parent.parent.parent
import sys
sys.path.insert(0, srcPath)

from scrape.job import config

from scrape import alphavantage as alphav

def job(symbols):
    """ Scrape job for stocks. Gets daily prices + SEC informations

    Args:
        symbols (str[]): list of stock symbols to extract data from
    """    
    # ------------- TIME SERIES --------------
    alphav.daily_download(symbols=symbols)
    # ------------- SEC FILINGS --------------
    alphav.income_statement_download(symbols=symbols)
    alphav.balance_sheet_download(symbols=symbols)
    alphav.cash_flow_download(symbols=symbols)
    alphav.earnings_download(symbols=symbols)

def crypto_job(symbols):
    """ Scrape job for crypto. Gets daily prices

    Args:
        symbols (str[]): list of crypto symbols to extract data from
    """    
    alphav.crypto_daily(symbols=symbols)

# start = time.time()
# if config.alphavConfig['market'] == 'stock':
#     job(symbols=config.alphavConfig['symbols'])
#     end = time.time()
#     print("Stock extraction took a total of "+str(end - start)+" seconds")
# elif config.alphavConfig['market'] == 'crypto':
#     crypto_job(symbols=config.alphavConfig['symbols'])
#     end = time.time()
#     print("Crypto extraction took a total of "+str(end - start)+" seconds")
# else:
#   'Something wrong with the configuration parameters, please make sure the input value is valid'