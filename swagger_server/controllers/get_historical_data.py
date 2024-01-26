from polygon import RESTClient
from datetime import datetime, timedelta
import pandas as pd
from flask import current_app
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date
import yfinance as yf

polygon_client = RESTClient(api_key=current_app.config['POLYGON_API_KEY'])

def get_historical_data_polygon(symbol,start,end):
  stock=pd.DataFrame(polygon_client.get_aggs(ticker=symbol, multiplier=1, timespan="day", from_=start, to=end,sort="asc", limit=50000))
  stock['Date']=(pd.to_datetime(stock['timestamp'],unit='ms')) 
  stock['Date'] = pd.to_datetime(stock['Date']).dt.date
  stock.set_index('Date', inplace=True)
  stock.drop(['timestamp', 'transactions','otc'], axis=1, inplace=True)
  stock.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume", "vwap": "Adj Close"}, inplace=True)
  return stock

def get_historical_data_yfinance(symbol,start,end):
  stock=yf.download(symbol, start=start, end=end)
  return stock