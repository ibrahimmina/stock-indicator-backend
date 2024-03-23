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

def get_start_dates(period,length, multiplier, frontend):
    back_period = process_period(period,multiplier,frontend)  
    if period == "minute":
        back_days = back_period + int(length/current_app.config['TRADING_MINUTE_PER_DAY']) + current_app.config['BACK_PERIOD_MINUTE']
    elif period == "week":
        back_days = back_period+(length*7)+(current_app.config['BACK_PERIOD']*7)
    elif period == "month":
        back_days = back_period+(length*30)+(current_app.config['BACK_PERIOD']*30)
    else:
        back_days = back_period+length+current_app.config['BACK_PERIOD']
    
    start=datetime.now() - timedelta(days=back_days)
    required_start = datetime.now() - timedelta(days=back_period)
    limit = process_limit(period,frontend)  
    return start, required_start,limit

def get_dates(period, multiplier, frontend):
    back_period = process_period(period,multiplier,frontend) 
    end=datetime.now()
    start= end - timedelta(days=back_period)
    limit = process_limit(period,frontend)      
    return start, end,limit

def process_period(period,multiplier,frontend):
    # Check if the DataFrame is empty
    if frontend in current_app.config['PERIOD_DICT']:
        if period in current_app.config['PERIOD_DICT'][frontend]:
            return current_app.config['PERIOD_DICT'][frontend][period] * multiplier
        else:
            raise CustomException(f"The specified period is not configured",404)
    else:
        raise CustomException(f"The specified period is not configured",404)

def process_limit(period,frontend):
    # Check if the DataFrame is empty
    if frontend in current_app.config['LIMIT_DICT']:
        if period in current_app.config['LIMIT_DICT'][frontend]:
            return current_app.config['LIMIT_DICT'][frontend][period]
        else:
            raise CustomException(f"The specified period is not configured",404)
    else:
        raise CustomException(f"The specified period is not configured",404)