import time

from elk import setup

start = time.time()
setup.create_index(slug="crypto_news")
setup.create_index(slug="balance_sheet")
setup.create_index(slug="cash_flow")
setup.create_index(slug="crypto_news")
setup.create_index(slug="daily_crypto")
setup.create_index(slug="daily_stock")
setup.create_index(slug="earning_calls")
setup.create_index(slug="earnings")
setup.create_index(slug="income_statement")
setup.create_index(slug="stocktwits")
end = time.time()
print("Elasticsearch index creation took a total of "+str(end - start)+" seconds")