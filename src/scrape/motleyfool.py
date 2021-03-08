"""
Motley Fool provides transcripts of the most recent earnings calls for the companies that they cover.  Information directly from the company on their operating performance.
"""

from bs4 import BeautifulSoup

from utils import logger, request
from elk import ingest

# Elastic search index
elasticPath = "http://localhost:9200/earning_calls/ingest"

def ec_list_download(startPage=1, endPage=10):
    """ Get a list of earning calls transcripts urls

    Args:
        startPage (int): start page
        endPage (int): end page

    Returns:
        str[]: list of earning calls urls
    """        
    urlList = []
    baseUrl = "https://www.fool.com/earnings-call-transcripts/?page="
    for page in range(startPage,endPage+1):
        url = baseUrl+str(page)
        response, logInfo = request.get(url=url, timeout = 120)
        if response.status_code == 200:
            logger.debug(logInfo+' - SUCCESS!')
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
        else:
            logger.error(logInfo+' - FAILED with error code '+response.status_code+' and message '+response.text)
            logger.info("Skipping page "+page+" because request failed...")
    return urlList

def ec_transcript_download(href, title):
    """ Get a single earning call transcript from a url

        Beautiful Soup Parser. The earning calls content are all as follow:
            1) Prepared Remarks
            2) Questions and Answers
            3) Call Participants
            4) Meta-data such as duration, date, company name...

    Args:
        href (str): earning call transcript url
        title (str): earning call title
    """
    baseUrl = "https://www.fool.com"
    url = baseUrl + href
    response, logInfo = request.get(url=url, timeout = 120)
    if response.status_code == 200:
        logger.debug(logInfo+' - SUCCESS!')

        # fetch main article body
        soup = BeautifulSoup(response.text, 'html.parser')
        articleSoup = soup.find_all("section", {"class": "usmf-new article-body"})[0]

        # parse prepared remarks
        try:
            remarks = response.text.split("Prepared Remarks:")[1].split("Questions &amp; Answers:")[0].split("<br/> ")[1]
        except:
            remarks = response.text.split("Prepared Remarks:")[1].split("Questions and Answers:")[0].split("</h2>")[1]
            
        remarksSoup = BeautifulSoup(remarks, 'html.parser')
        elements = remarksSoup.find_all("p")
        function = ""
        speaker = ""
        finalRemark = []
        for elem in elements:
            if elem.find_all("em"):
                function = elem.find_all("em")[0].text
            if elem.find_all("strong"):
                speaker = elem.find_all("strong")[0].text
            else:
                content = elem.text
                if content:
                    phrase = {
                        "speaker": speaker,
                        "function": function,
                        "content": content
                    }
                    finalRemark.append(phrase)
        # parse questions and answers
        try:
            QAs = response.text.split("Questions &amp; Answers:")[1].split("[Operator signoff]")[0].split("<br/> ")[1]
        except:
            try:
                QAs = response.text.split("Questions and Answers:")[1].split("[Operator signoff]")[0].split("</h2>")[1]
            except:
                try:
                    QAs = response.text.split("Questions &amp; Answers:")[1].split("[Operator signoff]")[0].split("</h2>")[1]
                except:
                    logger.info("Skipping article: '"+title+"' because Q&A parsing failed failed...")
                    return

        QASoup = BeautifulSoup(QAs, 'html.parser')
        elements = QASoup.find_all("p")
        function = ""
        speaker = ""
        finalQA = []
        for elem in elements:
            if elem.find_all("em"):
                function = elem.find_all("em")[0].text
            if elem.find_all("strong"):
                speaker = elem.find_all("strong")[0].text
            else:
                content = elem.text
                if content:
                    phrase = {
                        "speaker": speaker,
                        "function": function,
                        "content": content
                    }
                    finalQA.append(phrase)
        # parse meta-data
        companyName = articleSoup.find_all("p")[1].find_all("strong")[0].text
        date = articleSoup.find(id="date").text
        time = articleSoup.find(id="time").text
        duration = response.text.split("Duration: ")[1].split("</strong>")[0]
        # parse call participants
        participantsStr = response.text.split("Call participants:")[1].split("<p><a href=")[0].split("</h2>")[1]
        participantsSoup = BeautifulSoup(participantsStr, 'html.parser')
        participantsSoup = participantsSoup.find_all("p")
        participants = []
        for participant in participantsSoup:
            if participant.find_all("strong") and participant.find_all("em"):
                name = participant.find_all("strong")[0].text
                function = participant.find_all("em")[0].text
                participants.append({
                    "name": name,
                    "function": function
                })
        # combine information
        finalDict = {
            "remarks": finalRemark,
            "QA": finalQA,
            "company": companyName,
            "title": title,
            "date": date,
            "time": time,
            "duration": duration,
            "participants": participants
        }
        # Ingest into Elastic Search
        ingest.ingest(post_url=elasticPath, payload=finalDict)
    else:
        logger.error(logInfo+' - FAILED with error code '+response.status_code+' and message '+response.text)
        logger.info("Skipping article: '"+title+"' because request failed...")

def all_transcripts_download(startPage=1, endPage=10):
    """ Scrape all earning calls given range

    Args:
        startPage (int, optional): start page. Defaults to 1.
        endPage (int, optional): end page. Defaults to 10.
    """
    # first fetch list of urls
    urlList = ec_list_download(startPage=startPage, endPage=endPage)
    page = 0
    # scrape each earning call in the list of urls
    for url in urlList:
        page = page + 1
        href = url['href']
        title = url['title']
        ec_transcript_download(href=href, title=title)
