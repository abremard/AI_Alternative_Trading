import os
import subprocess
import datetime
import logging
import urllib
import sys
import io

def log(logInfo):
    logging.debug(logInfo)

def log_config():
    # Log config
    pspath = os.path.abspath("log-retention.ps1")
    logpath = os.path.abspath("log")
    p = subprocess.Popen(["powershell.exe", 
                pspath, logpath], 
                stdout=sys.stdout)
    p.communicate()
    logDay = datetime.datetime.now().strftime('%d-%m-%Y')
    logging.basicConfig(filename='log/'+logDay+'.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
