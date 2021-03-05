import os
import subprocess
import datetime
import logging
import urllib
import sys
import pandas as pd
import io
import json
from bs4 import BeautifulSoup

from utils import logger, utils

def news_list_download(symbol, startPage, endPage):
    urlList = []
    for page in range(startPage,endPage+1):
        baseUrl = "https://www.coindesk.com/wp-json/v1/search?keyword="+symbol+"&page="
        url = baseUrl+str(page)
        response, logInfo = utils.request(url, "GET", timeout = 120)
        logger.log(logInfo)
        articleList = json.loads(response.content)['results']
        for article in articleList:
            title = article['slug']
            href = article['url']
            urlList.append({
                "href": href,
                "title": title
            })
    return urlList

def article_download(href, title):
    url = href
    response, logInfo = utils.request(url, "GET", timeout = 120)
    logger.log(logInfo)
    article = response.text
    article = article.split('"articleBody":')[1].split('"')[1].split('"')[0]
    with open("./data/crypto/news/"+title+".txt", "w", encoding="utf8") as file:
        file.write(article)

def all_articles_download(symbol, startPage=1, endPage=10):
    urlList = news_list_download(symbol=symbol, startPage=startPage, endPage=endPage)
    for url in urlList:
        href = url['href']
        title = url['title']
        article_download(href=href, title=title)