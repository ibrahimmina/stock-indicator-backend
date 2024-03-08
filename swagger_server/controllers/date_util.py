from flask import current_app
from datetime import datetime, timedelta, date
from swagger_server.exceptions import CustomException
import pandas as pd

def check_date_greater_today(target_date):
    if target_date > datetime.now():
        raise CustomException(f"The specified date is greater than today",405)

def get_end_date():
    end=datetime.now()
    return end

def get_historical_start_date(period):
    back_period = process_period(period)
    start=datetime.now() - timedelta(days=back_period+current_app.config['BACK_PERIOD'])
    return start

def get_required_start_date(period):
    back_period = process_period(period)
    required_start = datetime.now() - timedelta(days=back_period)
    return start

def get_start_dates(period):
    back_period = process_period(period)
    start=datetime.now() - timedelta(days=back_period+current_app.config['BACK_PERIOD'])
    required_start = datetime.now() - timedelta(days=back_period)
    return start, required_start

def process_period(period):
    # Check if the DataFrame is empty
    if period not in current_app.config['PERIOD_DICT']:
        raise CustomException(f"The specified period is not configured",404)
    else:
      return current_app.config['PERIOD_DICT'][period]