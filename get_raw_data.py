from alpha_vantage.timeseries import TimeSeries
import datetime
from datetime import date

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import pandas as pd

def get_raw_data(key_value, stock):
    ts = TimeSeries(key=key_value, output_format='pandas')
    stock_data_bi_weekly, meta_data = ts.get_intraday(symbol=stock, outputsize='full') #get all data

    end_date = datetime.datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d") 
    added_weeks = datetime.timedelta(days=14) #set interval to be the last two weeks
    start_date = ( end_date - added_weeks ).strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    stock_date_filter = stock_data_bi_weekly[(stock_data_bi_weekly.index > start_date) & (stock_data_bi_weekly.index <= end_date)] #get data for the last two weeks
    stock_date_filter = stock_date_filter.sort_index(ascending=True)

    stock_date_filter_sub = stock_date_filter[["1. open", "4. close", "5. volume"]].astype(dtype=float) #get only the required columns

    stock_date_filter_sub = stock_date_filter_sub.rename(columns={"1. open": "open_price", "4. close": "close_price", "5. volume": "volume"}) #rename columns
    stock_date_filter_sub["symbol"] = [stock] * len(stock_date_filter_sub)
    stock_date_filter_sub["date"] = stock_date_filter_sub.index.strftime('%Y-%m-%d')

    ordered_cols = ["symbol", "date", "open_price", "close_price", "volume"]
    stock_date_filter_sub = stock_date_filter_sub[ordered_cols]
    stock_date_filter_sub.index = range(len(stock_date_filter_sub))

    stock_date_filter_sub = stock_date_filter_sub[["symbol", "date", "open_price", "close_price", "volume"]]
    return stock_date_filter_sub


IBM_date_filter_sub = get_raw_data('OKXM9T3K23QCCSGO', 'IBM')
Apple_date_filter_sub = get_raw_data('OKXM9T3K23QCCSGO', 'AAPL')

total_financial_data = pd.concat([IBM_date_filter_sub, Apple_date_filter_sub], axis=0)

total_financial_data.to_json('./stock_data.json', orient='records', indent=1, lines=True)
total_financial_data.to_csv('./stock_data.csv', sep=',')

conn = None
try: 
    conn_string = "host='localhost' dbname='local_db' user='postgres' password='locpass'"
    conn = psycopg2.connect(conn_string)
    print("Connected to the database successfully")

    cursor = conn.cursor();

    date_filter_df = pd.read_csv("./stock_data.csv", sep=',')        
    date_filter_list = []
    for index, rows in date_filter_df.iterrows():
        #get the current row
        temp_list =[rows.symbol, rows.date, rows.open_price, rows.close_price, rows.volume]      
        # append the list to the final list
        date_filter_list.append(temp_list)

    sql_query  ='INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (symbol, date, open_price, close_price, volume) DO NOTHING';
    cursor.executemany(sql_query, date_filter_list)
    conn.commit()
    print("records inserted successfully")
    cursor = conn.cursor()
    conn.close()
    
except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
    if conn is not None:
        conn.close()    


