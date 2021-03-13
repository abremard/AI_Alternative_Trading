"""
Python pprint module wrapper
"""

import pprint

def print(stuff="", indent=4, compact=True, width=200):
    """ Pretty print string given as parameter

    Args:
        stuff (str, optional): string to print. Defaults to "".
        indent (int, optional): print indentation. Defaults to 4.        
    """
    pp = pprint.PrettyPrinter(indent=indent, compact=compact, width=width)
    pp.pprint(stuff)