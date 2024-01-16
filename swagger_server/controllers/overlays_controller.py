import connexion
import six

from swagger_server.models.bollinger import Bollinger  # noqa: E501
from swagger_server.models.ema import Ema  # noqa: E501
from swagger_server.models.sma import Sma  # noqa: E501
from swagger_server import util


def calculate_bollinger_bands(symbol, start_date, period, length=None, standard_deviation=None):  # noqa: E501
    """An oscillator meaning that it operates between or within a set range of numbers or parameters..

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: The short period
    :type length: int
    :param standard_deviation: The long period
    :type standard_deviation: int

    :rtype: Bollinger
    """
    return 'do some magic!'


def calculate_ema(symbol, start_date, period, length=None):  # noqa: E501
    """The average price over the specified period

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: The short period
    :type length: int

    :rtype: Ema
    """
    return 'do some magic!'


def calculate_sma(symbol, start_date, period, length=None):  # noqa: E501
    """The average price over the specified period

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: The short period
    :type length: int

    :rtype: Sma
    """
    return 'do some magic!'
