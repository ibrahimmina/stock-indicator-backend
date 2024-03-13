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
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date, get_required_start_date, process_period, get_start_dates
from swagger_server.controllers.df_util import cleandfupdated

USE_POLYGON = current_app.config['USE_POLYGON']

def calculate_adl(symbol, period):  # noqa: E501
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
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        adl = stock.ta.ad(high=stock['High'], low=stock['Low'], close=stock['Close'], volume=stock['Volume'])
        
        output = cleandfupdated(adl,stock, required_start, end, 2,"_.*$")

        output = Adl.from_dict(output.to_dict(orient='records'))
        
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_adx(symbol, period, length=None, scalar=None, drift=None, lensig=None):  # noqa: E501
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
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        adx = stock.ta.adx(high=stock['High'], low=stock['Low'], close=stock['Close'], length=length, lensig=lensig, scalar=scalar, drift=drift)
        
        output = cleandfupdated(adx,stock, required_start, end, 2,"_.*$")

        output = Adx.from_dict(output.to_dict(orient='records'))
        
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500


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
    try:
        start = get_historical_start_date(start_date,length)
        end = get_end_date(start_date,period)
        required_start = get_required_start_date(start_date)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon(symbol,start,end)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        bbands = stock.ta.bbands(close="Close", std=standard_deviation, length=length).dropna()
        bbands = pd.merge(stock, bbands, left_index=True, right_index=True)
        bbands.columns = bbands.columns.str.replace("_*.\d", "", regex=True)
        bbands = bbands.drop(['BBB', 'BBP','Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        
        bbands = bbands.loc[required_start.date():end.date()]
        bbands = bbands.round(2)
        
        bbands['Date'] = pd.to_datetime(bbands.index.astype(str), format='%Y-%M-%d')
        bbands['Date'] = bbands['Date'].dt.strftime('%Y-%M-%d')

        output = Bollinger(bbands['Date'].values.tolist(), bbands['BBL'].values.tolist(), bbands['BBM'].values.tolist(), bbands['BBU'].values.tolist(), bbands['Close'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_bollinger_bands_updated(symbol, period, length=5, standard_deviation=2):  # noqa: E501
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

        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        bbands = stock.ta.bbands(close="Close", std=standard_deviation, length=length).dropna()
        bbands = pd.merge(stock, bbands, left_index=True, right_index=True)
        bbands.columns = bbands.columns.str.replace("_*.\d", "", regex=True)
        bbands = bbands.drop(['BBB', 'BBP','Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        
        bbands = bbands.loc[required_start.date():end.date()]
        bbands = bbands.round(2)

        bbands.dropna(inplace=True)

        output = Bollinger(bbands['timestamp'].values.tolist(), bbands['BBL'].values.tolist(), bbands['BBM'].values.tolist(), bbands['BBU'].values.tolist(), bbands['Close'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_ema(symbol, period, length=5):  # noqa: E501
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
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        ema = stock.ta.ema(close="Close", length=length).dropna()
        outputdf = pd.merge(stock, ema, left_index=True, right_index=True)
        jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        jsondf.columns = jsondf.columns.str.replace("^EMA_*[0-9]*", "EMA", regex=True)
        
        jsondf = jsondf.loc[required_start.date():end.date()]
        jsondf = jsondf.round(2)   
        
        #jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
        #jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

        jsondf.dropna(inplace=True)

        output = Ema(jsondf['timestamp'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['EMA'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500




def calculate_sma(symbol, period, length=5):  # noqa: E501
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
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)

        sma = stock.ta.sma(close="Close", length=length).dropna()
        outputdf = pd.merge(stock, sma, left_index=True, right_index=True)
        jsondf = outputdf.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
        jsondf.columns = jsondf.columns.str.replace("^SMA_*[0-9]*", "SMA", regex=True)

        jsondf = jsondf.loc[required_start.date():end.date()]
        jsondf = jsondf.round(2)

        #jsondf['Date'] = pd.to_datetime(jsondf.index.astype(str), format='%Y-%M-%d')
        #jsondf['Date'] = jsondf['Date'].dt.strftime('%Y-%M-%d')

        jsondf.dropna(inplace=True)

        output = Sma(jsondf['timestamp'].values.tolist(), jsondf['Close'].values.tolist(), jsondf['SMA'].values.tolist())

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500