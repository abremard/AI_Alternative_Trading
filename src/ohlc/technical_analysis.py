""" Feature engineering using a wrapper for Technical Analysis package
"""

from pathlib import Path
parent = Path(__file__).resolve().parent
srcPath = str(parent.parent).replace("\\", "\\\\")
import sys
sys.path.insert(0, srcPath)

import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna

from elk import search

def all_features(dataframe):
    """ Compute technical features using Technical Analysis package

    Args:
        dataframe (Dataframe.Object): raw dataframe

    Returns:
        Dataframe.Object: dataframe with additional features
    """    
    # Map column labels
    labels = {
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'adjusted_close',
        'volume': 'volume',
    }
    # Delete unecessary columns
    del dataframe['close']
    del dataframe['dividend_amount']
    del dataframe['split_coefficient']
    del dataframe['day']
    # Clean NaN values
    df = dropna(dataframe)
    # Add ta features filling NaN values
    return add_all_ta_features(df, open=labels['open'], high=labels['high'], low=labels['low'], close=labels['close'], volume=labels['volume'], fillna=True)