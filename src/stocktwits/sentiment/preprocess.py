""" Preprocess stocktwits data
"""

from transformers import BertTokenizer
import json
import pandas as pd
import random
import tensorflow as tf

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

from utils import prettyprint as pp
from elk import search
from stocktwits.bert import tokenize
 
def map_doc_to_dict(input_ids, attention_masks, token_type_ids, label):
    """ Map to the expected input to TFBertForSequenceClassification

    Args:
        input_ids (int[]): tokenized word ids
        attention_masks (int[]]): attention mask to not focus on pad tokens 
        token_type_ids (int[]):
        label (int[]): classification label, 0 for Bearish, 1 for Bullish

    Returns:
        Dict: mapped document
    """    
    return {
        "input_ids": input_ids,
        "token_type_ids": token_type_ids,
        "attention_mask": attention_masks,
    }, label

def parse(elastic_docs):
    """ Keep only body, sentiment and id for binary classification

    Args:
        elastic_docs (Dict): document fetched from elasticsearch index

    Returns:
        Dict: parsed document
    """    
    docs = []
    # iterate each Elasticsearch doc in list
    for num, doc in enumerate(elastic_docs):
        # get _source data dict from document
        source_data = doc["_source"]
        # get _id from document
        _id = source_data["id"]
        # bert data will only contain data useful for sentiment analysis
        filtered_data = {}
        filtered_data['body'] = source_data['body']
        if source_data['entities']['sentiment'] is not None:
            if source_data['entities']['sentiment']['basic'] is not None:
                filtered_data['sentiment'] = source_data['entities']['sentiment']['basic']
                filtered_data['id'] = _id
        # append the Series object to the DataFrame object
        docs.append(filtered_data)
    return docs

def encode(input_ids_list, attention_mask_list, token_type_ids_list, label_list):
    """ Encode data into a tensorflow Dataset

    Args:
        input_ids (int[]): tokenized word ids
        attention_masks (int[]]): attention mask to not focus on pad tokens 
        token_type_ids (int[]):
        label (int[]): classification label, 0 for Bearish, 1 for Bullish

    Returns:
        tf.Dataset.Object: encoded dict
    """    
    return tf.data.Dataset.from_tensor_slices((input_ids_list, attention_mask_list, token_type_ids_list, label_list)).map(map_doc_to_dict)

def export_elastic_docs(elastic_docs, filename):
    """ Export elasticsearch results to json and csv files

    Args:
        elastic_docs (Dict): input object
        filename (str): output path
    """    
    with open(filename+'.json', 'w') as f:
        json.dump(elastic_docs, f)

    docs = pd.DataFrame()

    documents = parse(elastic_docs=elastic_docs)

    for document in documents:
        # create a Series object from doc dict object
        doc_data = pd.Series(document, name=document['id'])
        # append the Series object to the DataFrame object
        docs = docs.append(doc_data)
        
    docs.to_csv(filename+'.csv')
    
def preprocess(train_size, max_length, batch_size):
    """ Shuffle, tokenize, clean up and encode

    Args:
        train_size (int): how much of the labelled data is used for training, the rest will be used for testing
        max_length (int): max sentence length in tokens
        batch_size (int): training batch size

    Returns:
        tf.Dataset.Object, tf.Dataset.Object: train_dataset, test_dataset
    """    
    bullishResults = search.bullish_stocktwits()
    bearishResults = search.bearish_stocktwits()
    labelledResults = bullishResults + bearishResults
    unlabelledResults = search.unlabelled_stocktwits()
    labelledResults = parse(elastic_docs=labelledResults)
    unlabelledResults = parse(elastic_docs=unlabelledResults)
    
    # Shuffle data
    random.shuffle(labelledResults)
    random.shuffle(unlabelledResults)
    
    # export_elastic_docs(elastic_docs=bullishResults,filename="./bullish")
    # export_elastic_docs(elastic_docs=bearishResults,filename="./bearish")
    # export_elastic_docs(elastic_docs=unlabelledResults,filename="./unlabelled")
    
    # Tokenize
    tokenizer = tokenize.init_tokenizer()
    
    # prepare list, so that we can build up final TensorFlow dataset from slices.
    input_ids_list = []
    token_type_ids_list = []
    attention_mask_list = []
    label_list = []
    
    for result in labelledResults:
        sentence = result['body']
        bert_input = tokenize.tokenizer_plus(tokenizer=tokenizer, sentence=sentence, max_length=max_length)
        input_ids_list.append(bert_input['input_ids'])
        token_type_ids_list.append(bert_input['token_type_ids'])
        attention_mask_list.append(bert_input['attention_mask'])
        if result['sentiment'] == "Bullish":
            label_list.append([1])
        else:
            label_list.append([0])
            
    encoded = encode(input_ids_list, attention_mask_list, token_type_ids_list, label_list).batch(batch_size) 
    
    return encoded.take(train_size), encoded.skip(train_size)