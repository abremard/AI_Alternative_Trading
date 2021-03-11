"""
Flipside makes available its asset rating score, FCAS, in addition to several other high-level value metrics that track Developer Activity, Blockchain Utility and Market Maturity.
"""

import json
import time

from utils import logger, request
from elk import ingest

api_key = "e0ed45af-7b62-4ceb-a118-1050779f03f8"
baseUrl = "https://api.flipsidecrypto.com/api/v2/"
# Elastic search index
elasticPath = "http://localhost:9200/crypto_score/ingest"

def api_req(url, rtype, formData=None):
    """ Flipside API wrapper. For more information please refer to: https://api-docs-v2.flipsidecrypto.com/ 

    Args:
        url (str): endpoint url
        rtype (str): request type, can only be "GET" or "POST"
        formData (dict, optional): python dict containing post form payload data. Defaults to None.

    Returns:
        requests.Response Object
    """
    # Sleeps for 5 seconds
    time.sleep(5)
    finalUrl = baseUrl + url + "?api_key=" + api_key
    formData = json.dumps(formData)
    if rtype == "POST":
        response, logInfo = request.post(url=finalUrl, timeout=120, referer=None, formData=formData)
    elif rtype == "GET":
        response, logInfo = request.get(url=finalUrl, timeout=120)
    return response, logInfo

def get_projects(symbol):
    url = "metrics/projects"
    response, logInfo = api_req(url=url, rtype="GET")
    id = "none"
    if response.status_code == 200:
        logger.debug(logInfo+' - SUCCESS!')
        projects = json.loads(response.content)["data"]
        for project in projects:
            if project["symbol"] == symbol:
                id = project["id"]
                break
    else:
        logger.error(logInfo+' - FAILED with error code '+str(response.status_code)+' and message '+response.text)
        logger.info("Skipping "+symbol+" because request failed...")
    return id

def timeseries_metrics(project_ids, metrics, start_timestamp, end_timestamp, period):
    """ Returns timeseries rating data for a given set of Metrics and Project IDs.
        Developer Score: A daily composite score representing the amount and type of work being done on a product. This score tracks activity across three major categories: changes to the codebase, major releases and updates, and community involvement.
        FCAS: A proprietary rating derived from the activity of developers, on chain behaviors and market activity.
        Market Maturity Score: Market Maturity, derived from Risk and Money Supply factors, represents the likelihood a crypto asset will provide consistent returns across various market scenarios by combining assessments of market risk (specifically, exchange liquidity, price projections, price cliff potential, algorithmic prediction consistency, and price volatility), as well as an analysis of the stability of the Money Supply of each tracked project. The less stable the Money Supply, and the more controlled it is by a few addresses, the worse the Money Supply score.
        Utility Score: A distilled representation of non-exchange related economic activity. Computed daily.

    Args:
        project_ids (str[]): list of flipside unique symbol identifier, for example ["7d9f417d-6646-4545-a992-48289a52f80c"] 
        metrics (str[]): list of metric slugs to download, for example ["fcas"]
        start_timestamp (str): beginning of timeseries range, for example "2018-01-01T00:00:00Z"
        end_timestamp (str): end of timeseries range, for example "2018-01-08T00:00:00Z"
        period (str): period of time serie, for example "day" 
    """    
    url = "metrics/timeseries/projects"

    formData = dict(
                    project_ids = project_ids,
                    metrics = metrics,
                    start_timestamp = start_timestamp,
                    end_timestamp = end_timestamp,
                    period = period
                    )
    response, logInfo = api_req(url=url, rtype="POST", formData=formData)
    if response.status_code == 200:
        logger.debug(logInfo+' - SUCCESS!')
        for project in json.loads(response.content)["data"]:
            symbol = project["symbol"]
            metrics = project["metrics"]
            for metric in metrics:
                metricName = metric["name"]
                for daily in metric["timeseries"]:
                    daily["metric"] = metricName
                    ingest.ingest(post_url=elasticPath, payload=daily)
    else:
        logger.error(logInfo+' - FAILED with error code '+str(response.status_code)+' and message '+response.text)
        logger.info(f"Skipping {str(project_ids).encode(encoding='UTF-8',errors='strict')} because request failed...")

def metrics_download(projects, metrics, start_timestamp, end_timestamp, period = "day"):
    """ Returns timeseries rating data for a given set of Metrics and Project names.

    Args:
        project (str[]): list of symbols/projects, for example ["BTC"] 
        metrics (str[]): list of metric slugs to download, for example ["fcas"]
        start_timestamp (str): beginning of timeseries range, for example "2018-01-01T00:00:00Z"
        end_timestamp (str): end of timeseries range, for example "2018-01-08T00:00:00Z"
        period (str): period of time serie, for example "day" 
    """    
    project_ids = []
    i = 0
    for project in projects:
        project_id = get_projects(project)
        if project_id != "none":
            project_ids.append(project_id)
            i = i + 1
    timeseries_metrics(project_ids=project_ids, metrics=metrics, start_timestamp=start_timestamp, end_timestamp=end_timestamp, period=period)

def job(projects):
    """ Scrape job

    Args:
        projects (str[]): list of crypto projects, for example ["BTC"]
    """    
    metrics = ['dev', 'fcas', 'market-maturity', 'utility']
    start_timestamp = "2019-01-01T00:00:00Z"
    end_timestamp = "2021-01-01T00:00:00Z"
    period = "day"
    metrics_download(projects=projects, metrics=metrics, start_timestamp=start_timestamp, end_timestamp=end_timestamp, period=period)
