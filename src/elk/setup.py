"""
Create an elastic search index with the given slug, if the index exists then first delete it.
This code was inspired by the original works of Dinesh Sonachalam: https://github.com/dineshsonachalam/Building-a-search-engine-using-Elasticsearch/blob/master/scraper.py
"""

import requests
import json

def check_if_index_is_present(url):
    """ Check if elastic search index exists

    Args:
        url (str): elastic search index url

    Returns:
        JSON Object: response object
    """    
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data

def create_index(slug):
    """ Create index given a slug

    Args:
        slug (str): index name
    """    
    url = "http://localhost:9200/_template/"+slug+"/"
    response = requests.request("GET", url, data="")
    if(len(response.text)>2):
        print("Deleted template: "+slug)
        response_delete = requests.request("DELETE", url)
    payload = {
          "template": slug,
          "settings": {
            "number_of_shards": 1
          },
          "mappings": {
            "ingest":{
                "_source": {
                    "enabled": True
                },
                "properties":{
                }
            }

          }
    }
    payload = json.dumps(payload)
    headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
    response = requests.request("PUT", url, data=payload, headers=headers)

    url = "http://localhost:9200/"+slug
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        print("Deleted an index: "+slug)
        response = requests.request("DELETE", url)

    response = requests.request("PUT", url)
    if (response.status_code == 200):
        print("Created an index: "+slug)
