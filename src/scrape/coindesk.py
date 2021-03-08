"""
CoinDesk is the media platform for the next generation of investors exploring how cryptocurrencies and digital assets are contributing to the evolution of the global financial system. Its mandate is to inform, educate, and connect the global investment community through news, data, events and education.
"""

import json

from utils import logger, request
from elk import ingest

# Elastic search index
elasticPath = "http://localhost:9200/crypto_news/ingest"

def news_list_download(symbol, startPage, endPage):
    """ Download list of news url that will later be scraped 

    Args:
        symbol (str): symbol used in the search parameter, for example "btc"
        startPage (int): start page
        endPage (int): end page

    Returns:
        List of Dicts: list of urls and their meta data
    """    
    urlList = []
    for page in range(startPage,endPage+1):
        baseUrl = "https://www.coindesk.com/wp-json/v1/search?keyword="+symbol+"&page="
        url = baseUrl+str(page)
        response, logInfo = request.get(url, timeout = 120)
        if response.status_code == 200:
            logger.debug(logInfo+' - SUCCESS!')
            articleList = json.loads(response.content)['results']
            for article in articleList:
                title = article['title']
                slug = article['slug']
                date = article['date']
                author = article['author']
                href = article['url']
                urlList.append({
                    "href": href,
                    "title": title,
                    "slug": slug,
                    "date": date,
                    "author": author
                })
        else:
            logger.error(logInfo+' - FAILED with error code '+response.status_code+' and message '+response.text)
            logger.info("Skipping page "+page+" because request failed...")
    return urlList

def article_download(url, title, slug, date, author):
    """ Download a single news article given its url

    Args:
        url (string): url of news article
        title (string): human-readable title of news article
        slug (string): computer-readable title of news article
        date (string): publication date
        author (string[]): list of authors
    """    
    response, logInfo = request.get(url, timeout = 120)
    if response.status_code == 200:
        logger.debug(logInfo+' - SUCCESS!')
        article = response.text
        article = article.split('"articleBody":')[1].split('"')[1].split('"')[0]
        payload = {
            "title": title,
            "slug": slug,
            "content": article,
            "date": date,
            "author": author
        }
        # Ingest into Elastic Search
        ingest.ingest(post_url=elasticPath, payload=payload)
    else:
        logger.error(logInfo+' - FAILED with error code '+response.status_code+' and message '+response.text)
        logger.info("Skipping article: '"+title+"' because request failed...")

def all_articles_download(symbol, startPage=1, endPage=10):
    """ Download a list of news articles about a given symbol

    Args:
        symbol (str): symbol, for example "btc"
        startPage (int, optional): start page. Defaults to 1.
        endPage (int, optional): end page. Defaults to 10.
    """    
    urlList = news_list_download(symbol=symbol, startPage=startPage, endPage=endPage)
    for url in urlList:
        href = url['href']
        title = url['title']
        slug = url['slug']
        date = url['date']
        author = url['author']
        article_download(href=href, title=title, slug=slug, date=date, author=author)