from flask import current_app
from datetime import datetime, timedelta, date
from swagger_server.exceptions import CustomException

def check_date_greater_today(target_date):
    if target_date > datetime.now():
        raise CustomException(f"The specified date is greater than today",405)

def get_end_date(start_date,period):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    check_date_greater_today(input_start)
    end = input_start + timedelta(days=period)
    check_date_greater_today(end)
    return end

def get_historical_start_date(start_date,length=0):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    check_date_greater_today(input_start)
    start = input_start - timedelta(days=length+current_app.config['BACK_PERIOD'])
    return start

def get_required_start_date(start_date,length=0):
    input_start = datetime.strptime(start_date, "%Y-%m-%d")
    check_date_greater_today(input_start)
    start = input_start
    return start