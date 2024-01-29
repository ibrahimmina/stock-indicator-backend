import connexion
import six

from swagger_server.models.cci import Cci  # noqa: E501
from swagger_server.models.efi import Efi  # noqa: E501
from swagger_server.models.mfi import Mfi  # noqa: E501
from swagger_server.models.obv import Obv  # noqa: E501
from swagger_server.models.roc import Roc  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from flask import current_app, jsonify
from swagger_server.exceptions import CustomException


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_yfinance
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date, get_required_start_date

USE_POLYGON = current_app.config['USE_POLYGON']

def calculate_cci(symbol, start_date, period, length=14, cci_scaling_constant=0.015):  # noqa: E501
    """Used to help determine when an investment vehicle is reaching a condition of being overbought or oversold.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: period length
    :type length: float
    :param cci_scaling_constant: scaling constant
    :type cci_scaling_constant: float

    :rtype: Cci
    """
    try:
        start = get_historical_start_date(start_date,length)
        end = get_end_date(start_date,period)
        required_start = get_required_start_date(start_date)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon(symbol,start,end)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        cci = stock.ta.cci(high="High",low="Low",close="Close", c=cci_scaling_constant, length=length)
       
        jsondf = cci.loc[start.date():end.date()]
        jsondf = jsondf.round(2)


        output = Cci.from_dict(jsondf.to_json(date_format='iso'))
        return output
    except Exception as e:
        return jsonify({'error': str(e)}), e.response_code or 500


def calculate_efi(symbol, start_date, period, length=None):  # noqa: E501
    """Elder&#x27;s Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: diff period
    :type length: float

    :rtype: Efi
    """
    return 'do some magic!'


def calculate_mfi(symbol, start_date, period, length=None):  # noqa: E501
    """The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure over a specified period of time.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: diff period
    :type length: float

    :rtype: Mfi
    """
    return 'do some magic!'


def calculate_obv(symbol, start_date, period):  # noqa: E501
    """The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure over a specified period of time.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int

    :rtype: Obv
    """
    return 'do some magic!'


def calculate_roc(symbol, start_date, period, length=None):  # noqa: E501
    """Elder&#x27;s Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: How much to magnify
    :type length: float

    :rtype: Roc
    """
    return 'do some magic!'
