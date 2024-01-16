import connexion
import six

from swagger_server.models.bollinger import Bollinger  # noqa: E501
from swagger_server.models.ema import Ema  # noqa: E501
from swagger_server.models.sma import Sma  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta

from polygon import RESTClient

def get_historical_data_polygon(symbol,start_date,period,length):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    start = input_start - timedelta(days=length+1)
    end = input_start + timedelta(days=period)
    client = RESTClient(trace=True)
    stock = client.list_aggs(symbol,1,"day",start,end)
    return stock

def get_historical_data(symbol,start_date,period,length):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    start = input_start - timedelta(days=length+1)
    end = input_start + timedelta(days=period)
    stock=yf.download(symbol, start=start, end=end)
    return stock

def calculate_bollinger_bands(symbol, start_date, period, length=5, standard_deviation=2):  # noqa: E501
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

    stock=get_historical_data(symbol, start_date,period,length)
    bbands = stock.ta.bbands(close="Close", std=standard_deviation, length=length).dropna()
    bbands = pd.merge(stock, bbands, left_index=True, right_index=True)
    bbands.columns = bbands.columns.str.replace("_*.\d", "", regex=True)
    bbands = bbands.drop(['BBB', 'BBP','Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    bbands['Date'] = pd.to_datetime(bbands.index.astype(str), format='%Y-%M-%d')
    bbands['Date'] = bbands['Date'].dt.strftime('%Y-%M-%d')

    output = Bollinger(bbands['Date'].values.tolist(), bbands['BBL'].values.tolist(), bbands['BBM'].values.tolist(), bbands['BBU'].values.tolist(), bbands['Close'].values.tolist())

    return output


def calculate_ema(symbol, start_date, period, length=5):  # noqa: E501
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

    stock=get_historical_data(symbol, start_date,period,length)
    ema = stock.ta.ema(close="Close", length=length).dropna()
    outputdf = pd.merge(stock, ema, left_index=True, right_index=True)
    jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    jsondf.columns = jsondf.columns.str.replace("^EMA_*[0-9]*", "EMA", regex=True)
    jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
    jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

    output = Ema(jsondf['Date'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['EMA'].values.tolist())

    return output

def calculate_sma(symbol, start_date, period, length=5):  # noqa: E501
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


    stock=get_historical_data(symbol, start_date,period,length)
    print(stock)
    sma = stock.ta.sma(close="Close", length=length).dropna()
    outputdf = pd.merge(stock, sma, left_index=True, right_index=True)
    jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
    jsondf.columns = jsondf.columns.str.replace("^SMA_*[0-9]*", "SMA", regex=True)
    jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
    jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

    output = Sma(jsondf['Date'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['SMA'].values.tolist())

    return output