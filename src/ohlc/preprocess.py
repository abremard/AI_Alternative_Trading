""" Preprocessor for technical analysis
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

import pandas as pd

from elk import search
from ohlc import technical_analysis as ta

def parse(elastic_docs):
    """ Parse price data to dataframe

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dataframe.Object: parsed document
    """    
    
    documents = []
    docs = pd.DataFrame()
    
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # append the Series object to the DataFrame object
        doc_data = pd.Series(source_data, name=source_data['day'])
        docs = docs.append(doc_data)
    
    docs.open = pd.to_numeric(docs.open, errors='coerce').astype(float)
    docs.high = pd.to_numeric(docs.high, errors='coerce').astype(float)
    docs.low = pd.to_numeric(docs.low, errors='coerce').astype(float)
    docs.adjusted_close = pd.to_numeric(docs.adjusted_close, errors='coerce').astype(float)
    docs.volume = pd.to_numeric(docs.volume, errors='coerce').astype(float)
    
    return docs

def preprocess():
    """ Load data from elasticsearch, parse into dataframe and compute features
    """    
    # Load data from elastic search to dataframe
    elastic_docs = search.price_data(size=500)
    df = parse(elastic_docs=elastic_docs)
    # Compute features
    df = ta.all_features(dataframe=df)
    
# preprocess()