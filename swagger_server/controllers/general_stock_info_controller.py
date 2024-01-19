import connexion
import six

from swagger_server.models.candlestick import Candlestick  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta

def get_historical_data(symbol,start_date,period):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    start = input_start
    end = input_start + timedelta(days=period)
    stock=yf.download(symbol, start=start, end=end)
    return stock

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

    stock=get_historical_data(symbol, start_date,period)
    stock['Date'] = pd.to_datetime(stock.index.astype(str), format='%Y-%M-%d')
    stock['Date'] = stock['Date'].dt.strftime('%Y-%M-%d')

    output = Candlestick(stock['Date'].values.tolist(), stock['Close'].values.tolist(), stock['Open'].values.tolist(), stock['High'].values.tolist(), stock['Low'].values.tolist(),stock['Volume'].values.tolist(), stock['Adj Close'].values.tolist())

    return output
