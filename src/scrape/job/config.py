""" Python scraping job config file
"""
# Below are configutations for stocktwits job
stwitsConfig = dict(
    symbol = 'MSFT',
    elasticPath = "http://localhost:9200/stocktwits/ingest",
)
# Below are configutations for alphavantage job
alphavConfig = dict(
    market = 'stock', # or 'crypto'
    symbols = ["IBM", "AAPL", "AMGN", "GOOG", "AMZN", "EBAY", "MSFT", "NFLX", "NVDA"],
    # stock
    dailyPriceIndex = "http://localhost:9200/daily_stock/ingest",
    incomeStatementIndex = "http://localhost:9200/income_statement/ingest",
    balanceSheetIndex = "http://localhost:9200/balance_sheet/ingest",
    cashFlowIndex = "http://localhost:9200/cash_flow/ingest",
    earningsIndex = "http://localhost:9200/earnings/ingest",
    # crypto
    dailyCryptoIndex = "http://localhost:9200/daily_crypto/ingest",
)