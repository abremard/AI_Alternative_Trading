""" Load stocktwits data """

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from utils import prettyprint as pp

import pandas as pd
import csv, json
import numpy as np
from elasticsearch import Elasticsearch

# create a client instance of the library
elastic_client = Elasticsearch()

def search(index, body={}, size=10):
    """ Search elasticsearch

    Args:
        index (str): index names
        body (dict, optional): query body. Defaults to {}
        size (int, optional): result limit size. Defaults to 10

    Returns:
        Dict: returned object body
    """    
    # make an API call to the Elasticsearch cluster to get documents
    return elastic_client.search(index=index, body=body, size=size)["hits"]["hits"]

def price_data(symbols, size=10000):
    """ Collect OHLC data
    Args:
        symbols (str[]): list of symbols to extract data from
        size (int, optional): result limit size. Defaults to 10000.

    Returns:
        Dataframe.Object: dataframe containing price data
    """    
    body = {
        "query" : {
            "bool" : {
                "filter" : {
                    "terms" : {
                        "symbol.keyword": symbols
                    }
                }
            }
        }
    }
    return search(index="daily_stock", body=body, size=size)

def balance_sheet(symbols, size=10000):
    """ Collect balance sheet data
    Args:
        symbols (str[]): list of symbols to extract data from
        size (int, optional): result limit size. Defaults to 10000.

    Returns:
        Dataframe.Object: dataframe containing price data
    """    
    body = {
        "query" : {
            "bool" : {
                "filter" : {
                    "terms" : {
                        "symbol.keyword": symbols
                    }
                }
            }
        }
    }
    return search(index="balance_sheet", body=body, size=size)

def cash_flow(symbols, size=10000):
    """ Collect cash flow data
    Args:
        symbols (str[]): list of symbols to extract data from
        size (int, optional): result limit size. Defaults to 10000.

    Returns:
        Dataframe.Object: dataframe containing price data
    """    
    body = {
        "query" : {
            "bool" : {
                "filter" : {
                    "terms" : {
                        "symbol.keyword": symbols
                    }
                }
            }
        }
    }
    return search(index="cash_flow", body=body, size=size)

def earnings(symbols, size=10000):
    """ Collect earnings data
    Args:
        symbols (str[]): list of symbols to extract data from
        size (int, optional): result limit size. Defaults to 10000.

    Returns:
        Dataframe.Object: dataframe containing price data
    """    
    body = {
        "query" : {
            "bool" : {
                "filter" : {
                    "terms" : {
                        "symbol.keyword": symbols
                    }
                }
            }
        }
    }
    return search(index="earnings", body=body, size=size)

def income_statement(symbols, size=10000):
    """ Collect income statement data
    Args:
        symbols (str[]): list of symbols to extract data from
        size (int, optional): result limit size. Defaults to 10000.

    Returns:
        Dataframe.Object: dataframe containing price data
    """    
    body = {
        "query" : {
            "bool" : {
                "filter" : {
                    "terms" : {
                        "symbol.keyword": symbols
                    }
                }
            }
        }
    }
    return search(index="income_statement", body=body, size=size)

def bullish_stocktwits(size=100):
    """ Collect stocktwits with Bullish label
    Args:
        size (int, optional): result limit size. Defaults to 100.

    Returns:
        Dict: list of bullish stocktwits
    """    
    body = {
        "query" : {
            "bool" : {
            "filter" : {
                "terms" : {
                "entities.sentiment.basic.keyword": ["Bullish"]
                }
            }
            }
        }
    } # match labelled stocktwits
    return search(index="stocktwits", body=body, size=size)

def bearish_stocktwits(size=100):
    """ Collect stocktwits with Bearish label
    Args:
        size (int, optional): result limit size. Defaults to 100.

    Returns:
        Dict: list of bearish stocktwits
    """     
    body = {
        "query" : {
            "bool" : {
            "filter" : {
                "terms" : {
                "entities.sentiment.basic.keyword": ["Bearish"]
                }
            }
            }
        }
    } # match labelled stocktwits
    return search(index="stocktwits", body=body, size=size)    

def unlabelled_stocktwits(size=100):
    """ Collect stocktwits with no label
    Args:
        size (int, optional): result limit size. Defaults to 100.

    Returns:
        Dict: list of stocktwits
    """     
    body = {
        "query" : {
            "bool" : {
            "must_not" : {
                "terms" : {
                "entities.sentiment.basic.keyword": ["Bullish", "Bearish"]
                }
            }
            }
        }
    } # match labelled stocktwits
    return search(index="stocktwits", body=body, size=size)

def stocktwits_by_symbols(symbols, gte, lte, size=100):
    """ Collect stocktwits with no label
    Args:
        size (int, optional): result limit size. Defaults to 100.

    Returns:
        Dict: list of stocktwits
    """     
    body = {
        "query" : {
            "bool" : {
                "filter" : [{
                    "terms" : {
                        "symbols.symbol.keyword": symbols
                    }
                },{
                    "range": {
                        "created_at": {
                            "gte": gte, 
                            "lte": lte        
                        }
                    }
                }]
            }
        }
    } # match labelled stocktwits
    return search(index="stocktwits", body=body, size=size)