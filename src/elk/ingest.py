"""
Ingest payload data to an elastic search index
"""

import json
import requests

from utils import logger

def ingest(post_url, payload):
    """ Ingest function

    Args:
        post_url (str): index url, for example "http://localhost:9200/stocktwits/ingest"
        payload (JSON Object): data to ingest in elastic search
    """    
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    payload = json.dumps(payload)
    response = requests.request("POST", post_url, data=payload, headers=headers)
    if(response.status_code==201):
        logger.debug(f'SUB TASK - POST - {post_url} - SUCCESS!')
    else:
        logger.error(f'SUB TASK - POST - {post_url} - FAILED with error code '+response.status_code+' and message '+response.text)