""" Preprocess stocktwits data for tweets scoring
"""

import pandas as pd
import numpy as np
import datetime

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from utils import prettyprint as pp
from elk import search

def parse(elastic_docs, symbol):
    """ Keep useful info for tweets scoring

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index
        symbol (str): symbol of the stock to score

    Returns:
        Dataframe.Object: document parsed into dataframe
    """
    docs = pd.DataFrame() 
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # get _id from document
        _id = source_data["id"]
        # bert data will only contain data useful for sentiment analysis
        source_data["user_id"] = source_data["user"]["id"]
        source_data["user_username"] = source_data["user"]["username"]
        source_data["user_name"] = source_data["user"]["name"]
        source_data["user_join_date"] = source_data["user"]["join_date"]
        source_data["user_followers"] = source_data["user"]["followers"]
        source_data["user_following"] = source_data["user"]["following"]
        source_data["user_official"] = source_data["user"]["official"]
        source_data["user_ideas"] = source_data["user"]["ideas"]
        source_data["user_watchlist"] = source_data["user"]["watchlist_stocks_count"]
        source_data["user_like_count"] = source_data["user"]["like_count"]
        source_data["source_title"] = source_data["source"]["title"]
        source_data["source_url"] = source_data["source"]["url"]
        source_data["symbol"] = symbol
        if source_data["user"]["plus_tier"] != "":
            source_data["user_plus_tier"] = 1.0
        else:
            source_data["user_plus_tier"] = 0.0
        if source_data["user"]["premium_room"] != "":
            source_data["user_premium_room"] = 1.0
        else:
            source_data["user_premium_room"] = 0.0
        if source_data['entities']['sentiment'] is not None:
            if source_data['entities']['sentiment']['basic'] is not None:
                source_data['sentiment'] = source_data['entities']['sentiment']['basic']
        try:
            source_data["likes_count"] = source_data["likes"]["total"]
            source_data["likes_ids"] = source_data["likes"]["user_ids"]
            del source_data["likes"]
        except:
            pass
        try:
            source_data["reshared_count"] = source_data["reshares"]["reshared_count"]
            source_data["reshared_user_ids"] = source_data["reshares"]["user_ids"]
            del source_data["reshares"]
        except:
            pass
        try:
            del source_data["reshare_message"]
        except:
            pass            
        try:
            source_data["is_parent"] = source_data["conversation"]["parent"]
            source_data["replies_count"] = source_data["conversation"]["replies"]
            del source_data["conversation"]
        except:
            pass
        try:
            del source_data["links"]
        except:
            pass
        del source_data["source"]
        del source_data["entities"]
        del source_data["symbols"]
        del source_data["user"]
        doc_data = pd.Series(source_data, name=source_data['created_at'])
        del doc_data["created_at"]
        docs = docs.append(doc_data)
    return docs

def normalize(df):
    """ Normalize numeric columns, affect them with their weight and sum them into final tweet score

    Args:
        df (Dataframe.Object): dataframe containing numeric values and boolean values. Some columns contain boolean values so they won't need normalization, but they still count in the score.

    Returns:
        Dataframe.Object: normalized dataframe
    """    
    normalize_columns = ["likes_count", "user_followers", "user_following", "user_ideas", "user_like_count", "user_watchlist", "replies_count", "reshared_count", "timedelta"]
    columns = ["likes_count", "user_followers", "user_following", "user_ideas", "user_like_count", "user_watchlist", "replies_count", "reshared_count", "timedelta", "user_plus_tier", "user_premium_room", "user_official"]
    weights = [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    result = df.copy()
    
    # fill empty values
    result[normalize_columns] = result[normalize_columns].fillna(value=0.0)
    
    # normalization loop
    for index, feature_name in enumerate(normalize_columns):
        # standard score normalization
        result[feature_name] = (result[feature_name] - result[feature_name].mean())/result[feature_name].std(ddof=0)

    # column weighting loop
    for index, feature_name in enumerate(columns):
        result[feature_name] = weights[index] * result[feature_name]

    # sum into score
    result['score'] = result[columns].sum(axis=1)
    
    # min-max normalization
    max_value = result['score'].max()
    min_value = result['score'].min()
    result['score'] = (result['score'] - min_value) / (max_value - min_value)
    
    return result

def compute_score(dataframe):
    """ Calculate tweet score by first normalizing the numeric features and then sum them using their weight

    Args:
        dataframe (Dataframe.Object): parsed dataframe

    Returns:
        Dataframe.Object: dataframe containing normalized columns and final score
    """    
    # timedelta
    for index, row in dataframe.iterrows():
        date = datetime.datetime.strptime(index, "%Y-%m-%dT%H:%M:%SZ")
        join_date = datetime.datetime.strptime(row['user_join_date'], "%Y-%m-%d")
        delta = (date - join_date).days
        dataframe.at[index, 'timedelta'] = delta
    # normalize
    dataframe = normalize(df=dataframe)
    return dataframe
    
def preprocess():
    """ Fetch data from elasticsearch, parse it and compute score
    """
    # day that needs to be studied
    date = datetime.datetime(2021, 2, 24)
    gte = date.strftime("%Y-%m-%dT%H:%M:%S")
    date += datetime.timedelta(days=1)
    lte = date.strftime("%Y-%m-%dT%H:%M:%S")
    # elasticsearch query
    results = search.stocktwits_by_symbols(symbols=["AMZN"], gte=gte, lte=lte, size=10000)
    # parsing
    df = parse(elastic_docs=results, symbol="AMZN")
    # df.to_csv("./test.csv")
    # score computing
    df = compute_score(dataframe=df)
    # df.to_csv("./test-comp.csv")

if __name__ == "__main__":
    preprocess()