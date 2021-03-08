"""
Python logging module wrapper with file retention system
"""

import os
import subprocess
import datetime
import logging
import sys

def debug(logInfo):
    """ DEBUG level log

    Args:
        logInfo (str): log message
    """    
    logging.debug(logInfo)

def info(logInfo):
    """ INFO level log

    Args:
        logInfo (str): log message
    """    
    logging.info(logInfo)

def error(logInfo):
    """ ERROR level log

    Args:
        logInfo (str): log message
    """    
    logging.error(logInfo)

def log_config():
    """ Initial logging configuration for project. 1 file for 1 day. Log message is appended to the file of current day. Retention is set in the powershell script.
    """    
    # Log config
    pspath = os.path.abspath("log-retention.ps1")
    logpath = os.path.abspath("log")
    p = subprocess.Popen(["powershell.exe", 
                pspath, logpath], 
                stdout=sys.stdout)
    p.communicate()
    logDay = datetime.datetime.now().strftime('%d-%m-%Y')
    logging.basicConfig(filename='log/'+logDay+'.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
