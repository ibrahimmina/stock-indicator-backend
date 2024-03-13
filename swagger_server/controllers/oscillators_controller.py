import connexion
import six

from swagger_server.models.cci import Cci  # noqa: E501
from swagger_server.models.cmf import Cmf  # noqa: E501

from swagger_server.models.efi import Efi  # noqa: E501
from swagger_server.models.macd import Macd  # noqa: E501

from swagger_server.models.mfi import Mfi  # noqa: E501
from swagger_server.models.obv import Obv  # noqa: E501
from swagger_server.models.ppo import Ppo  # noqa: E501
from swagger_server.models.psar import Psar  # noqa: E501
from swagger_server.models.pvo import Pvo  # noqa: E501
from swagger_server.models.roc import Roc  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from flask import current_app, jsonify
from swagger_server.exceptions import CustomException


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_yfinance, get_historical_data_polygon_updated
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date, get_required_start_date, get_start_dates
from swagger_server.controllers.df_util import cleandf, cleandfupdated

USE_POLYGON = current_app.config['USE_POLYGON']


def calculate_cci(symbol, period, length=14, cci_scaling_constant=0.015):  # noqa: E501
    """Used to help determine when an investment vehicle is reaching a condition of being overbought or oversold.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: period length
    :type length: float
    :param cci_scaling_constant: scaling constant
    :type cci_scaling_constant: float

    :rtype: Cci
    """
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        cci = stock.ta.cci(high=stock['High'], low=stock['Low'], close=stock['Close'], c=cci_scaling_constant, length=length)

        df = cci.to_frame()
        
        output = cleandfupdated(df, stock, required_start, end, 2,"_.*$")
        
        output = Cci.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_cmf(symbol, period, length=20):  # noqa: E501
    """Chailin Money Flow measures the amount of money flow volume over a specific period in conjunction with Accumulation/Distribution.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param length: period length
    :type length: float

    :rtype: Cmf
    """
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        cmf = stock.ta.cmf(high=stock['High'], low=stock['Low'], close=stock['Close'],open_=stock['Open'], length=length)

        df = cmf.to_frame()
        
        output = cleandfupdated(df,stock, required_start, end, 2,"_.*$")
        
        output = Cmf.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500    

def calculate_efi(symbol, period, length=13, drift=1):  # noqa: E501
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
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        efi = stock.ta.efi(close=stock['Close'], volume=stock['Volume'], length=length, drift=drift)

        df = efi.to_frame()

        output = cleandfupdated(df, stock, required_start, end, 2,"_.*$")

        output = Efi.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500


def calculate_macd(symbol, period, fast=12, slow=26, signal=9):  # noqa: E501
    """The MACD is a popular indicator to that is used to identify a security&#x27;s trend. While APO and MACD are the same calculation, MACD also returns two more series called Signal and Histogram. The Signal is an EMA of MACD and the Histogram is the difference of MACD and Signal.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param fast: The short period
    :type fast: float
    :param slow: The long period
    :type slow: float
    :param signal: The signal period
    :type signal: float

    :rtype: Macd
    """
    length=30
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        
        macd = stock.ta.macd(close=stock['Close'],fast=fast, slow=slow, signal=signal)

        output = cleandfupdated(macd, stock, required_start, end, 2,"_.*$")
            
        output = Macd.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500   


def calculate_mfi(symbol, period, length=14, drift=1):  # noqa: E501
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
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        mfi = stock.ta.mfi(high=stock['High'], low=stock['Low'], close=stock['Close'],volume=stock['Volume'], length=length, drift=drift)

        df = mfi.to_frame()
        output = cleandfupdated(df,stock, required_start, end, 2,"_.*$")
        output = Mfi.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_obv(symbol, period):  # noqa: E501
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
    length=0
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        obv = stock.ta.obv(close=stock['Close'],volume=stock['Volume'])

        df = obv.to_frame()

        output = cleandfupdated(df, stock,required_start, end, 2,"_.*$")
        

        output = Obv.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_psar(symbol, period, initial_acceleration=None, acceleration=None, max_acceleration=None):  # noqa: E501
    """An oscillator meaning that it operates between or within a set range of numbers or parameters..

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param initial_acceleration: The psar initial acceleration
    :type initial_acceleration: float
    :param acceleration: The psar acceleration
    :type acceleration: float
    :param max_acceleration: The psar max acceleration
    :type max_acceleration: float

    :rtype: Psar
    """
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        psar = stock.ta.psar(high=stock['High'], low=stock['Low'], close=stock['Close'],af0=0.02,af=0.02,max_af=0.2)

        output = cleandfupdated(psar, stock,required_start, end, 2,"_.*$")
        
        output = Psar.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500
            
def calculate_ppo(symbol, period, fast=None, slow=None, signal=None, scalar=None):  # noqa: E501
    """The Percentage Price Oscillator is similar to MACD in measuring momentum.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param fast: The short period
    :type fast: float
    :param slow: The long period
    :type slow: float
    :param signal: The signal period
    :type signal: float
    :param scalar: How much to magnify
    :type scalar: float

    :rtype: Ppo
    """
    
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        ppo = stock.ta.ppo(close=stock['Close'], fast=fast, slow=slow, signal=signal, scalar=scalar)

        output = cleandfupdated(ppo, stock,required_start, end, 2,"_.*$")
        
        output = Ppo.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_pvo(symbol, period, fast=None, slow=None, signal=None, scalar=None):  # noqa: E501
    """Percentage Volume Oscillator is a Momentum Oscillator for Volume.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param start_date: Start Date of Analysis in YYYY-MM-DD Format
    :type start_date: str
    :param period: The Analysis Period in Days from Start Date
    :type period: int
    :param fast: The short period
    :type fast: float
    :param slow: The long period
    :type slow: float
    :param signal: The signal period
    :type signal: float
    :param scalar: How much to magnify
    :type scalar: float

    :rtype: Pvo
    """

    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        pvo = stock.ta.pvo(volume=stock['Volume'], fast=fast, slow=slow, signal=signal, scalar=scalar)

        output = cleandfupdated(pvo, stock,required_start, end, 2,"_.*$")
        
        output = Pvo.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500



def calculate_roc(symbol, period, length=1, scalar=100):  # noqa: E501
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
    try:
        end = get_end_date()
        start, required_start = get_start_dates(period)

        if USE_POLYGON == True:
            stock=get_historical_data_polygon_updated(symbol,start,end, period)
        else:
            stock=get_historical_data_yfinance(symbol,start,end)
        
        roc = stock.ta.roc(close=stock['Close'],length=length, scalar=scalar)

        df = roc.to_frame()

        output = cleandfupdated(df, stock, required_start, end, 2,"_.*$")

        output = Roc.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500