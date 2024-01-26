from flask import current_app
from datetime import datetime, timedelta

def get_end_date(start_date,period):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    end = input_start + timedelta(days=period)
    return end

def get_historical_start_date(start_date,length=0):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    start = input_start - timedelta(days=length+current_app.config['BACK_PERIOD'])
    return start