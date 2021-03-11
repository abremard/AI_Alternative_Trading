"""
Ingest payload data to an elastic search index
"""

import json
import requests
import time

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
    for attempt in range(150):
        try:
            response = requests.request("POST", post_url, data=payload, headers=headers)
        except:
            logger.info(f'SUB TASK - POST - {post_url} - FAILED, retrying...')
            time.sleep(2)
        else:
            break
    if(response.status_code==201):
        logger.debug(f'SUB TASK - POST - {post_url} - SUCCESS!')
    else:
        logger.error(f'SUB TASK - POST - {post_url} - FAILED with error code '+str(response.status_code)+' and message '+response.text)