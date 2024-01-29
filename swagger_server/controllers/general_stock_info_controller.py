import connexion
import six

from swagger_server.models.candlestick import Candlestick  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta
from flask import current_app, jsonify
from swagger_server.exceptions import CustomException


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_yfinance
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date, get_required_start_date

USE_POLYGON = current_app.config['USE_POLYGON']



def calculate_candlestick(symbol, start_date, period):  # noqa: E501
    """The average price over the specified period

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int

    :rtype: Candlestick
    """

    start = get_required_start_date(start_date)
    end = get_end_date(start_date,period)

    if USE_POLYGON == True:
        stock=get_historical_data_polygon(symbol,start,end)
    else:
        stock=get_historical_data_yfinance(symbol,start,end)

    stock['Date'] = pd.to_datetime(stock.index.astype(str), format='%Y-%M-%d')
    stock['Date'] = stock['Date'].dt.strftime('%Y-%M-%d')

    stock = stock.loc[start.date():end.date()]
    stock = stock.round(2)
    
    output = Candlestick(stock['Date'].values.tolist(), stock['Close'].values.tolist(), stock['Open'].values.tolist(), stock['High'].values.tolist(), stock['Low'].values.tolist(),stock['Volume'].values.tolist(), stock['Adj Close'].values.tolist())

    return output
