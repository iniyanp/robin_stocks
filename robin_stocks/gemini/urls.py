""" Module contains all the API endpoints """
from enum import Enum, auto

from robin_stocks.gemini.helper import get_sandbox_flag


class AutoName(Enum):
    """Automatically sets an enum value to be its name when using auto()"""

    def _generate_next_value_(name, start, count, last_values):
        return name


class Version(AutoName):
    """Enum for different version types"""
    v1 = auto()
    v2 = auto()


class URLS:
    """ Static class for holding all urls."""
    __base_url = "https://api.gemini.com/"
    __base_sandbox_url = "https://api.sandbox.gemini.com/"

    def __init__(self):
        raise NotImplementedError(
            "Cannot create instance of {0}".format(self.__class__.__name__))

    @classmethod
    def get_base_url(cls, version):
        if get_sandbox_flag():
            url = cls.__base_sandbox_url
        else:
            url = cls.__base_url

        return url + version.value + "/"

    # authentication.py
    @classmethod
    def heartbeat(cls):
        return cls.get_base_url(Version.v1) + "heartbeat"

    # crypto.py
    @classmethod
    def pubticker(cls, ticker):
        return cls.get_base_url(Version.v1) + "pubticker/{0}".format(ticker)

    @classmethod
    def ticker(cls, ticker):
        return cls.get_base_url(Version.v2) + "ticker/{0}".format(ticker)

    @classmethod
    def symbols(cls):
        return cls.get_base_url(Version.v1) + "symbols"

    @classmethod
    def symbol_details(cls, ticker):
        return cls.get_base_url(Version.v1) + "symbols/details/{0}".format(ticker)

    # orders.py
    @classmethod
    def mytrades(cls):
        return cls.get_base_url(Version.v1) + "mytrades"

    @classmethod
    def order_new(cls):
        return cls.get_base_url(Version.v1) + "order/new"