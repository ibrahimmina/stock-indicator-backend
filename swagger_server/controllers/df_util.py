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

def cleandfupdated(df,stock,start,end,round_number,clean_regex):
    tempDF = pd.merge(stock, df, left_index=True, right_index=True)
    tempDF = tempDF.drop(['Open', 'High', 'Low', 'Close','Adj Close', 'Volume'], axis=1)
    output = tempDF.loc[start.date():end.date()]
    output = output.round(round_number)
    output.columns = output.columns.str.replace(clean_regex, "", regex=True)
    output.dropna(inplace=True)
    return output