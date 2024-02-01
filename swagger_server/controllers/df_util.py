from flask import current_app
from datetime import datetime, timedelta, date
from swagger_server.exceptions import CustomException
import pandas as pd

def cleandf(df,start,end,round_number,clean_regex,required_date_time_format):
    output = df.loc[start.date():end.date()]
    output = output.round(round_number)
    output.columns = output.columns.str.replace(clean_regex, "", regex=True)
    output['Date'] = pd.to_datetime(output.index.astype(str), format=required_date_time_format)
    output['Date'] = output['Date'].dt.strftime(required_date_time_format)
    return output