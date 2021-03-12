""" Python scraping job config file
"""
# Below are configutations for stocktwits job
stwitsConfig = dict(
    symbol = 'NFLX',
    elasticPath = "http://localhost:9200/stocktwits/ingest",
)