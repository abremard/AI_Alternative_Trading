""" Main script for data extraction
"""

from utils import logger, request
from scrape import alphavantage as alphav
from scrape import motleyfool as mfool
from scrape import stocktwits as stwits
from scrape import flipside, coindesk
from elk import setup

# ----------------------------------------------------------------------------------------------------------------

# logger.log_config()

# ------------- ELASTIC SEARCH CREATE INDEX --------------

# slug = "crypto_news"
# setup.create_index(slug)

# ------------- EARNING CALLS --------------

# for i in range(5):
#     print("scraping from "+str(i*20+1)+" to "+str((i+1)*20))
#     mfool.all_transcripts_download(startPage=(i*20+1),endPage=((i+1)*20))
#     print(str(i*20+1)+" to "+str((i+1)*20)+" done!")
# mfool.all_transcripts_download(startPage=101,endPage=200)
# mfool.ec_transcript_download(href="/earnings/call-transcripts/2021/03/03/axon-enterprise-aaxn-q4-2020-earnings-call-transcr/", title="Agile Therapeutics (AGRX) Q4 2020 Earnings Call Transcript")

# ------------- TIME SERIES --------------

# symbols = ["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"]
# symbols = ["IBM"]
# symbols = ["BTC"]
# alphav.daily_download(symbols=symbols)
# alphav.crypto_daily(symbols=symbols)

# ------------- SEC FILINGS --------------

# alphav.income_statement_download(symbols)
# alphav.balance_sheet_download(symbols)
# alphav.cash_flow_download(symbols)
# alphav.earnings_download(symbols)

# ------------- STOCKTWITS --------------

# symbol = "AAL"
# stwits.extract(symbol=symbol, nb=50)
# stwits.extract(symbol=symbol, nb=50, params=294481182)

# ------------- FLIPSIDE est.2017 --------------

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

# coindesk.all_articles_download(symbol="btc", startPage=1, endPage=2)
