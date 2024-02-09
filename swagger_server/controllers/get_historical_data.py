from polygon import RESTClient
from datetime import datetime, timedelta
import pandas as pd
from flask import current_app
from swagger_server.controllers.date_util import get_end_date, get_historical_start_date
import yfinance as yf
from polygon.exceptions import AuthError, BadResponse
from swagger_server.exceptions import CustomException
from connexion.exceptions import OAuthProblem
import traceback
from urllib3.exceptions import MaxRetryError

polygon_client = RESTClient(api_key=current_app.config['POLYGON_API_KEY'])



def process_dataframe(df):
    # Check if the DataFrame is empty
    if df.empty:
        raise CustomException(f"The specified symbol was not found",404)

def get_historical_data_polygon(symbol,start,end):
  try:
    stock=pd.DataFrame(polygon_client.get_aggs(ticker=symbol, multiplier=1, timespan="day", from_=start, to=end,sort="asc", limit=50000))
    process_dataframe(stock)
    stock['Date']=(pd.to_datetime(stock['timestamp'],unit='ms')) 
    stock['Date'] = pd.to_datetime(stock['Date']).dt.date
    stock.set_index('Date', inplace=True)
    stock.drop(['timestamp', 'transactions','otc'], axis=1, inplace=True)
    stock.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume", "vwap": "Adj Close"}, inplace=True)
    return stock
  except AuthError as e:
    # Handle general Polygon.io exceptions
    raise CustomException(f"Polygon.io exception: {e}",401)
  except BadResponse as e:
    # Handle HTTP-related exceptions (e.g., network issues, API rate limits)
    raise CustomException(f"Polygon.io HTTP exception: {e}",405)
  except MaxRetryError as e:
    raise CustomException(f"Polygon.io HTTP exception: {e}",429)
  except CustomException as ce:
    raise CustomException(f"Unexpected exception: {ce}",ce.response_code)
  except Exception as e:
    # Handle other unexpected exceptions
    print (traceback.format_exc())
    raise CustomException(f"Unexpected exception: {e}",500)

def get_historical_data_yfinance(symbol,start,end):
  try:
    stock=yf.download(symbol, start=start, end=end)
    return stock
  except Exception as e:
    print (str(e))
    raise e