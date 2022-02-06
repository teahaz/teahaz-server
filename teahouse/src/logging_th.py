"""
Universal logging function for teahaz.

This module exports one logging class
with a few logging functions with different
levels of urgency.
"""


import sys
import time


class logger:
    """
        Logger class exports a few logging functions
        for different levels of urgency.
    """

    def __init__(self):
        self._PURPLE = '\033[95m'
        self._BLUE = '\033[94m'
        self._CYAN = '\033[96m'
        self._GREEN = '\033[92m'
        self._YELLOW = '\033[93m'
        self._RED = '\033[91m'
        self._BOLD = '\033[1m'
        self._UNDERLINE = '\033[4m'
        self._RESET = '\033[0m'


    def printf(self, function_name, prefix, message):
        """ Print formatted log """
        msg = prefix
        msg += f" {time.time()}".ljust(21, " ")
        msg += f"  ||  [{function_name.__module__}/{function_name.__name__}]  ||  "
        msg += message
        msg += self._RESET

        print(msg, file=sys.stderr)


    def succ(self, function_name, message: str):
        """ Success: Green bold text """
        prefix = self._RESET + self._BOLD + self._GREEN + self._UNDERLINE + "[ success ]".ljust(12, " ")
        self.printf(function_name=function_name, prefix=prefix, message=message)


    def log(self, function_name, message: str):
        """ Info: normal text """
        prefix = self._RESET + "[   log   ]".ljust(12, " ")
        self.printf(function_name=function_name, prefix=prefix, message=message)


    def warn(self, function_name, message: str):
        """ Warning: yellow text """
        prefix = self._RESET + self._YELLOW + "[ warning ]".ljust(12, " ")
        self.printf(function_name=function_name, prefix=prefix, message=message)


    def error(self, function_name, message: str):
        """ Error: Red bold text """
        prefix = self._RESET + self._BOLD + self._RED + "[  error  ]".ljust(12, " ")
        self.printf(function_name=function_name, prefix=prefix, message=message)

