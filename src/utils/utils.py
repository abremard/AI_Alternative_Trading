import requests

def request(url, rtype, timeout = 600, formData = None):
    if rtype == 'GET':
        log = f'SUB TASK - GET - {url}'
        page = requests.get(url=url,timeout=timeout, verify=False)
    elif rtype == 'POST':
        log = f'SUB TASK - POST - {url}'
        page = requests.post(url=url,data=formData,timeout=timeout,verify=False)
    return page, log