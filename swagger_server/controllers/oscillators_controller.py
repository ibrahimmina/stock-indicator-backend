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
from swagger_server.models.rsi import Rsi  # noqa: E501
from swagger_server.models.stoch import Stoch  # noqa: E501
from swagger_server import util

import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from flask import current_app, jsonify
from swagger_server.exceptions import CustomException


from swagger_server.controllers.get_historical_data import get_historical_data_polygon, get_historical_data_yfinance, get_historical_data_polygon_updated
from swagger_server.controllers.date_util import get_end_date, get_start_dates, get_dates
from swagger_server.controllers.df_util import cleandf, cleandfupdated, cleandffinal

USE_POLYGON = current_app.config['USE_POLYGON']


def calculate_cci(symbol, period, multiplier=1, frontend="Mobile", length=14, cci_scaling_constant=0.015):  # noqa: E501
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
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)

        
        cci = stock.ta.cci(high=stock['High'], low=stock['Low'], close=stock['Close'], c=cci_scaling_constant, length=length)

        df = cci.to_frame()
        
        output = cleandffinal(df, stock, 2,"_.*$", limit)
        
        output = Cci.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_cmf(symbol, period, multiplier=1, frontend="Mobile",length=20):  # noqa: E501
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
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        cmf = stock.ta.cmf(high=stock['High'], low=stock['Low'], close=stock['Close'],open_=stock['Open'], length=length)

        df = cmf.to_frame()
        
        output = cleandffinal(df,stock, 2,"_.*$", limit)
        
        output = Cmf.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500    

def calculate_efi(symbol, period, multiplier=1, frontend="Mobile",length=13, drift=1):  # noqa: E501
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
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        efi = stock.ta.efi(close=stock['Close'], volume=stock['Volume'], length=length, drift=drift)

        df = efi.to_frame()

        output = cleandffinal(df, stock, 2,"_.*$", limit)

        output = Efi.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500


def calculate_macd(symbol, period, multiplier=1, frontend="Mobile",fast=12, slow=26, signal=9):  # noqa: E501
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
    #length=30
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        
        macd = stock.ta.macd(close=stock['Close'],fast=fast, slow=slow, signal=signal)

        output = cleandffinal(macd, stock, 2,"_.*$", limit)
            
        output = Macd.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500   


def calculate_mfi(symbol, period, multiplier=1, frontend="Mobile",length=14, drift=1):  # noqa: E501
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
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        mfi = stock.ta.mfi(high=stock['High'], low=stock['Low'], close=stock['Close'],volume=stock['Volume'], length=length, drift=drift)

        df = mfi.to_frame()
        output = cleandffinal(df,stock, 2,"_.*$", limit)
        output = Mfi.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_obv(symbol, period,multiplier=1, frontend="Mobile"):  # noqa: E501
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
    #length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        obv = stock.ta.obv(close=stock['Close'],volume=stock['Volume'])

        df = obv.to_frame()

        output = cleandffinal(df, stock, 2,"_.*$", limit)
        
        output = Obv.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_psar(symbol, period, multiplier=1, frontend="Mobile",initial_acceleration=0.02, acceleration=0.02, max_acceleration=0.2):  # noqa: E501
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
    #length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        psar = stock.ta.psar(high=stock['High'], low=stock['Low'], close=stock['Close'],af0=initial_acceleration,af=acceleration,max_af=max_acceleration)

        output = cleandffinal(psar, stock, 2,"_.*$", limit)
        
        output = Psar.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500
            
def calculate_ppo(symbol, period, multiplier=1, frontend="Mobile",fast=12, slow=26, signal=9, scalar=100):  # noqa: E501
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
    #length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        ppo = stock.ta.ppo(close=stock['Close'], fast=fast, slow=slow, signal=signal, scalar=scalar)

        output = cleandffinal(ppo, stock, 2,"_.*$", limit)
        
        output = Ppo.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_pvo(symbol, period, multiplier=1, frontend="Mobile",fast=12, slow=26, signal=9, scalar=100):  # noqa: E501
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
    #length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        pvo = stock.ta.pvo(volume=stock['Volume'], fast=fast, slow=slow, signal=signal, scalar=scalar)

        output = cleandffinal(pvo, stock, 2,"_.*$", limit)
        
        output = Pvo.from_dict(output.to_dict(orient='records'))

        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500



def calculate_roc(symbol, period, multiplier=1, frontend="Mobile",length=1, scalar=100):  # noqa: E501
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
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        roc = stock.ta.roc(close=stock['Close'],length=length, scalar=scalar)

        df = roc.to_frame()

        output = cleandffinal(df, stock, 2,"_.*$", limit)

        output = Roc.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500

def calculate_rsi(symbol, period, multiplier=1, frontend="Mobile",length=14, scalar=100, drift=1):  # noqa: E501
    """The Relative Strength Index is popular momentum oscillator used to measure the velocity as well as the magnitude of directional price movements.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param period: The Analysis Period required
    :type period: str
    :param length: period length
    :type length: float
    :param scalar: How much to magnify
    :type scalar: float
    :param drift: The difference period
    :type drift: float

    :rtype: Rsi
    """
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        rsi = stock.ta.rsi(close=stock['Close'], length=length, scalar=scalar, drift=drift)

        df = rsi.to_frame()

        output = cleandffinal(df, stock, 2,"_.*$", limit)

        output = Rsi.from_dict(output.to_dict(orient='records'))
        
        return output

    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500


def calculate_stoch(symbol, period, multiplier=1, frontend="Mobile",fast=14, slow=3, smooth_k=3):  # noqa: E501
    """The Stochastic Oscillator (STOCH) was developed by George Lane in the 1950&#x27;s. He believed this indicator was a good way to measure momentum because changes in momentum precede changes in price.

     # noqa: E501

    :param symbol: Ticker Symbol Required
    :type symbol: str
    :param period: The Analysis Period required
    :type period: str
    :param k: The Fast %K period.
    :type k: float
    :param d: The Slow %K period.
    :type d: float
    :param smooth_k: The Slow %D period.
    :type smooth_k: float

    :rtype: Stoch
    """
    length=0
    try:
        #end = get_end_date()
        #start, required_start, limit = get_start_dates(period, length, multiplier=multiplier, frontend=frontend)

        start, end, limit = get_dates(period,multiplier,frontend)

        stock=get_historical_data_polygon_updated(symbol,start,end, period, multiplier)
        
        stoch = stock.ta.stoch(high=stock['High'],low=stock['Low'],close=stock['Close'],k=int(fast), d=int(slow), smooth_k=int(smooth_k))

        output = cleandffinal(stoch, stock, 2,"_.*$", limit)
            
        output = Stoch.from_dict(output.to_dict(orient='records'))
        return output
    except Exception as e:
        if hasattr(e,'response_code'):
            return jsonify({'error': str(e)}), e.response_code
        else:
            return jsonify({'error': str(e)}), 500   