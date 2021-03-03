from utils import logger, utils
from bs4 import BeautifulSoup

def ec_list_download(startPage=1, endPage=10):
    """Get earning calls transcripts lists
    """
    urlList = []
    for page in range(startPage,endPage):
        baseUrl = "https://www.fool.com/earnings-call-transcripts/?page="
        url = baseUrl+str(page)
        response, logInfo = utils.request(url, "GET", timeout = 120)
        logger.log(logInfo)
        soup = BeautifulSoup(response.text, 'html.parser')
        articleList = soup.find_all("a", {"data-id": "article-list"})
        for article in articleList:
            atag = str(article).split('<a')[1].split('>')[0]
            href = atag.split('href="')[1].split('"')[0]
            title = atag.split('title="')[1].split('"')[0]
            urlList.append({
                "href": href,
                "title": title
            })
    return urlList

def ec_transcript_download(href, title):
    """Get earning calls transcript from a url
    """
    baseUrl = "https://www.fool.com"
    url = baseUrl + href
    response, logInfo = utils.request(url, "GET", timeout = 120)
    logger.log(logInfo)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find_all("section", {"class": "usmf-new article-body"})[0]
    with open("./data/earning-calls/"+title+".html", "w") as file:
        file.write(str(article.prettify()))

def all_transcripts_download(startPage, endPage):
    urlList = ec_list_download(startPage=startPage, endPage=endPage)
    for url in urlList:
        href = url['href']
        title = url['title']
        ec_transcript_download(href=href, title=title)
