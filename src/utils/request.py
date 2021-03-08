"""
Python requests module wrapper with log message builder
"""

import requests
from fake_useragent import UserAgent
from selenium import webdriver

def get(url, timeout = 600, referer = None):
    """ HTTP GET Request

    Args:
        url (str): target url
        timeout (int, optional): timeout in seconds. Defaults to 600.
        referer (str, optional): referer. Defaults to None.

    Returns:
        requests.Response Object, str: response object, log message
    """    
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
    log = f'SUB TASK - GET - {url}'
    response = requests.get(url=url, timeout=timeout, headers=header, verify=False)
    return response, log

def post(url, timeout = 600, referer = None, formData = None):
    """ HTTP POST Request

    Args:
        url (str): target url
        timeout (int, optional): timeout in seconds. Defaults to 600.
        referer (str, optional): referer. Defaults to None.
        formData (JSON Object, optional): payload form data. Defaults to None.

    Returns:
        requests.Response Object, str: response object, log message
    """    
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
    log = f'SUB TASK - POST - {url}'
    response = requests.post(url=url, data=formData, timeout=timeout, headers=header, verify=False)
    return response, log

def selenium_request(url):
    """ Selenium request. WebDriver drives a browser natively, as a user would, either locally or on a remote machine using the Selenium server, marks a leap forward in terms of browser automation. Selenium WebDriver refers to both the language bindings and the implementations of the individual browser controlling code. This is commonly referred to as just WebDriver.

    Args:
        url (str): target url

    Returns:
        str: page source
    """    
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    return html