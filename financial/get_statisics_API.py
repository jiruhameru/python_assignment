from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datetime import datetime
import numpy as np
import math


app = Flask(__name__)
api = Api(app)

class Statistics(Resource):
    def get(self):
        args = request.args
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        symbol = args.get('symbol')

        result = None
        error = ''
        
        try:
            conn_string = "host='localhost' dbname='local_db' user='postgres' password='locpass'"
            conn = psycopg2.connect(conn_string)

            cursor = conn.cursor()
                
            if None not in (start_date, end_date, symbol):
                    
                # get the average daily open price resuts:
                average_daily_open_price_sql_query = "select row_to_json(t) as obj from (SELECT AVG(open_price) FROM financial_data WHERE symbol=%s AND date BETWEEN %s AND %s GROUP BY date) t;"                
                cursor.execute(average_daily_open_price_sql_query, (symbol,start_date,end_date))
            
                average_daily_open_price_rows = cursor.fetchall()                
                l1 = [x[0] for x in average_daily_open_price_rows]
                open_price_daily_averages = [av['avg'] for av in l1] #get the average values for each day                
                open_price_daily_average = np.round(np.mean(open_price_daily_averages), 2) #get the total daily average (scalar)
                if math.isnan(open_price_daily_average):
                    open_price_daily_average = 0
                

                # get the average daily close price resuts
                average_daily_close_price_sql_query = "select row_to_json(t) as obj from (SELECT AVG(close_price) FROM financial_data WHERE symbol=%s AND date BETWEEN %s AND %s GROUP BY date) t;"                
                cursor.execute(average_daily_close_price_sql_query, (symbol,start_date,end_date))

                average_daily_close_price_rows = cursor.fetchall()                
                l1 = [x[0] for x in average_daily_close_price_rows]
                close_price_daily_averages = [av['avg'] for av in l1] #get the average values for each day                
                close_price_daily_average = np.round(np.mean(close_price_daily_averages), 2) #get the total daily average (scalar)            
                if math.isnan(close_price_daily_average):
                    close_price_daily_average = 0

                # get the average daily volume resuts
                average_daily_volume_sql_query = "select row_to_json(t) as obj from (SELECT AVG(volume) FROM financial_data WHERE symbol=%s AND date BETWEEN %s AND %s GROUP BY date) t;"                
                cursor.execute(average_daily_volume_sql_query, (symbol,start_date,end_date))

                average_daily_volume_rows = cursor.fetchall()                
                l1 = [x[0] for x in average_daily_volume_rows]
                volume_daily_averages = [av['avg'] for av in l1] #get the average values for each day                
                volume_daily_average = np.round(np.mean(volume_daily_averages), 2) #get the total daily average (scalar)
                if math.isnan(volume_daily_average):
                    volume_daily_average = 0

                stat_dict = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'symbol': symbol, 
                    'average_daily_open_price': open_price_daily_average,
                    'average_daily_close_price': close_price_daily_average,
                    'average_daily_volume': volume_daily_average}            
                info_d = {'error': error}
                metdadata = {'data': stat_dict, 'info': info_d}
                                
                result = metdadata
        except (Exception, psycopg2.DatabaseError) as e:
                error = e
        finally:            
            if conn is not None:
                conn.close()    

        return result

api.add_resource(Statistics, '/api/statistics')

# Running the Local Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# http://localhost:5000/api/statistics?start_date=2023-02-10&end_date=2023-02-20&symbol=IBM

