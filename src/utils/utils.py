import requests
from fake_useragent import UserAgent
from selenium import webdriver

def request(url, rtype, timeout = 600, referer = None, formData = None):
    ua = UserAgent()
    if referer is not None:
        header = {
            "User-Agent": ua.random,
            "referer": referer
        }
    else:
        header = {
            "User-Agent": ua.random,
        }
    if rtype == 'GET':
        log = f'SUB TASK - GET - {url}'
        page = requests.get(url=url, timeout=timeout, headers=header, verify=False)
    elif rtype == 'POST':
        log = f'SUB TASK - POST - {url}'
        page = requests.post(url=url, data=formData, timeout=timeout, headers=header, verify=False)
    return page, log

def selenium_request(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    return html