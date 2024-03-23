import connexion
import six

from swagger_server.models.adl import Adl  # noqa: E501
from swagger_server.models.adx import Adx  # noqa: E501

from swagger_server.models.bollinger import Bollinger  # noqa: E501
from swagger_server.models.ema import Ema  # noqa: E501
from swagger_server.models.psar import Psar  # noqa: E501
from swagger_server.models.sma import Sma  # noqa: E502
from swagger_server import util

import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from flask import current_app, jsonify
from swagger_server.exceptions import CustomException


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_yfinance, get_historical_data_polygon_updated
from swagger_server.controllers.date_util import get_end_date, get_start_dates, get_dates
from swagger_server.controllers.df_util import cleandfupdated, cleandffinal

USE_POLYGON = current_app.config['USE_POLYGON']

def calculate_adl(symbol, period,multiplier=1, frontend="Mobile"):  # noqa: E501
    """Accumulation/Distribution indicator utilizes the relative position of the close to it&#x27;s High-Low range with volume.  Then it is cumulated.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int

    :rtype: Adl
    """
    #length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        adl = stock.ta.ad(high=stock['High'], low=stock['Low'], close=stock['Close'], volume=stock['Volume'])
        
        output = cleandffinal(adl,stock, 2,"_.*$", limit)

        output = Adl.from_dict(output.to_dict(orient='records'))
        
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_adx(symbol, period, multiplier=1, frontend="Mobile",length=14, scalar=100, drift=1, lensig=14):  # noqa: E501
    """Average Directional Movement is meant to quantify trend strength by measuring the amount of movement in a single direction.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: period length
    :type length: float
    :param scalar: How much to magnify
    :type scalar: float
    :param drift: diff period
    :type drift: float
    :param lensig: Signal Length
    :type lensig: float

    :rtype: Adx
    """
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        adx = stock.ta.adx(high=stock['High'], low=stock['Low'], close=stock['Close'], length=length, lensig=lensig, scalar=scalar, drift=drift)
        
        output = cleandffinal(adx,stock, 2,"_.*$", limit)

        output = Adx.from_dict(output.to_dict(orient='records'))
        
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500


def calculate_bollinger_bands_updated(symbol, period,multiplier=1, frontend="Mobile", length=5, standard_deviation=2):  # noqa: E501
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
    try:

        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)

        bbands = stock.ta.bbands(close="Close", std=standard_deviation, length=length)
        
        bbands = pd.merge(stock, bbands, left_index=True, right_index=True)
        bbands.columns = bbands.columns.str.replace("_.*$", "", regex=True)
        bbands = bbands.drop(['BBB', 'BBP','Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        
        #bbands = bbands.loc[required_start.date():end.date()]

        
        bbands = bbands.tail(limit)

        bbands = bbands.round(2)

        bbands.fillna(0,inplace=True)

        output = Bollinger(bbands['timestamp'].values.tolist(), bbands['BBL'].values.tolist(), bbands['BBM'].values.tolist(), bbands['BBU'].values.tolist(), bbands['Close'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_ema(symbol, period, multiplier=1, frontend="Mobile",length=5):  # noqa: E501
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
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        ema = stock.ta.ema(close="Close", length=length)
        outputdf = pd.merge(stock, ema, left_index=True, right_index=True)
        jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        jsondf.columns = jsondf.columns.str.replace("^EMA_*[0-9]*", "EMA", regex=True)
        
        #jsondf = jsondf.loc[required_start.date():end.date()]


        jsondf = jsondf.tail(limit)

        jsondf = jsondf.round(2)   
        
        #jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
        #jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

        jsondf.fillna(0,inplace=True)

        output = Ema(jsondf['timestamp'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['EMA'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500




def calculate_sma(symbol, period, multiplier=1, frontend="Mobile",length=5):  # noqa: E501
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
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)

        sma = stock.ta.sma(close="Close", length=length)
        outputdf = pd.merge(stock, sma, left_index=True, right_index=True)
        jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        jsondf.columns = jsondf.columns.str.replace("^SMA_*[0-9]*", "SMA", regex=True)

        #jsondf = jsondf.loc[required_start.date():end.date()]

        jsondf = jsondf.tail(limit)

        jsondf = jsondf.round(2)

        #jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
        #jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

        jsondf.fillna(0,inplace=True)

        output = Sma(jsondf['timestamp'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['SMA'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500