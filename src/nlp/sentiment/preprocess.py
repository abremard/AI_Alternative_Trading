""" Preprocess stocktwits data
"""

from transformers import BertTokenizer

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from utils import prettyprint as pp
from elk import search

import json
import pandas as pd

def export_elastic_docs(elastic_docs, filename):
    """ Export elasticsearch results to json and csv files

    Args:
        elastic_docs (Dict): input object
        filename (str): output path
    """    
    with open(filename+'.json', 'w') as f:
        json.dump(elastic_docs, f)

    docs = pd.DataFrame()

    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        
        # get _source data dict from document
        source_data = doc["_source"]
        
        # get _id from document
        _id = source_data["id"]
        
        # bert data will only contain data useful for sentiment analysis
        # TODO: calculate influence, quality... metrics and add on top of BERT vectors
        filtered_data = {}
        filtered_data['body'] = source_data['body']
        if source_data['entities']['sentiment'] is not None:
            if source_data['entities']['sentiment']['basic'] is not None:
                filtered_data['sentiment'] = source_data['entities']['sentiment']['basic']

        # create a Series object from doc dict object
        doc_data = pd.Series(filtered_data, name = _id)

        # append the Series object to the DataFrame object
        docs = docs.append(doc_data)
        
    docs.to_csv(filename+'.csv')
    
def main():
    bullishResults = search.bullish_stocktwits()
    bearishResults = search.bearish_stocktwits()
    unlabelledResults = search.unlabelled_stocktwits()
    # pp.print(bullishResults[:5])
    # pp.print(bearishResults[:5])
    # pp.print(unlabelledResults[:5])
    export_elastic_docs(elastic_docs=bullishResults,filename="./bullish")
    export_elastic_docs(elastic_docs=bearishResults,filename="./bearish")
    export_elastic_docs(elastic_docs=unlabelledResults,filename="./unlabelled")
    
# main()