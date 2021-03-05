import os
import subprocess
import datetime
import logging
import urllib
import sys
import pandas as pd
import io
import json

from utils import logger, utils

def api_req(url, rtype, formData=None):
    api_key = "e0ed45af-7b62-4ceb-a118-1050779f03f8"
    baseUrl = "https://api.flipsidecrypto.com/api/v2/"
    finalUrl = baseUrl + url + "?api_key=" + api_key
    formData = json.dumps(formData)
    if rtype == "POST":
        page, logInfo = utils.request(url=finalUrl, rtype="POST", timeout=120, referer=None, formData=formData)
    elif rtype == "GET":
        page, logInfo = utils.request(url=finalUrl, rtype="GET", timeout=120)
    logger.log(logInfo)
    return page

def get_projects(symbol):
    url = "metrics/projects"
    page = api_req(url=url, rtype="GET")
    projects = json.loads(page.content)["data"]
    id = "none"
    for project in projects:
        if project["symbol"] == symbol:
            id = project["id"]
            break
    return id

def timeseries_metrics(project_ids, metrics, start_timestamp, end_timestamp, period):
    url = "metrics/timeseries/projects"
    formData = dict(
                    project_ids = project_ids,
                    metrics = metrics,
                    start_timestamp = start_timestamp,
                    end_timestamp = end_timestamp,
                    period = period
                    )
    page = api_req(url=url, rtype="POST", formData=formData)
    for project in json.loads(page.content)["data"]:
        symbol = project["symbol"]
        outputPath = "./data/crypto/rating/"+symbol+".json"
        with open(outputPath, "w", encoding="utf8") as outf:
            outf.write(json.dumps(project))


def metrics_download(projects, metrics, start_timestamp, end_timestamp, period = "day"):
    project_ids = []
    i = 0
    for project in projects:
        project_id = get_projects(project)
        if project_id != "none":
            project_ids.append(project_id)
            i = i + 1
    timeseries_metrics(project_ids=project_ids, metrics=metrics, start_timestamp=start_timestamp, end_timestamp=end_timestamp, period=period)