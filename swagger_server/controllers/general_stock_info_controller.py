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


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_polygon_updated, get_historical_data_yfinance
from swagger_server.controllers.date_util import get_end_date, get_start_dates, get_dates

USE_POLYGON = current_app.config['USE_POLYGON']

def calculate_candlestick_updated(symbol, period, multiplier=1, frontend="Mobile"):  # noqa: E501
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
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length=0, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)
        
        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        if len(stock) > limit:
            stock = stock.tail(limit)

        stock = stock.round(2)

        stock.dropna(inplace=True)
        
        output = Candlestick(stock['timestamp'].values.tolist(), stock['Close'].values.tolist(), stock['Open'].values.tolist(), stock['High'].values.tolist(), stock['Low'].values.tolist(),stock['Volume'].values.tolist(), stock['Adj Close'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500