from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datetime import datetime
import os 

app = Flask(__name__)
api = Api(app)

class FinancialData(Resource):
    def get(self):
        args = request.args
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        symbol = args.get('symbol')
        limit = args.get('limit')
        page = args.get('page')


        result = None
        error = ''

        try:
            conn_string = "host='localhost' dbname='local_db' user='postgres' password='locpass'"
            conn = psycopg2.connect(conn_string)

            cursor = conn.cursor()
                
            if (limit is None):
                limit = 5
            if (page is None):
                page = 1
            offset = int(page) * int(limit)
            if(symbol is None):                
                sql_query = "select row_to_json(t) as obj from (SELECT symbol, date, open_price, close_price, volume FROM financial_data LIMIT %s OFFSET %s) t;"
                cursor.execute(sql_query, (limit, offset))                
            elif (start_date is None or end_date is None):
                sql_query = "select row_to_json(t) as obj from (SELECT symbol, date, open_price, close_price, volume FROM financial_data WHERE symbol=%s LIMIT %s OFFSET %s) t;"
                cursor.execute(sql_query, (symbol, limit, offset))
            elif None not in (symbol,start_date,end_date, limit, offset): 
                sql_query = "select row_to_json(t) as obj from (SELECT symbol, date, open_price, close_price, volume FROM financial_data WHERE symbol=%s AND date BETWEEN %s AND %s LIMIT %s OFFSET %s) t;"
                cursor.execute(sql_query, (symbol,start_date,end_date, limit, offset))
            
            rows = cursor.fetchall()                            

            cursor_all = conn.cursor()
            sql_query_count = "select row_to_json(t) as obj from (SELECT symbol, date, open_price, close_price, volume FROM financial_data WHERE symbol=%s AND date BETWEEN %s AND %s) t;"
            cursor_all.execute(sql_query_count, (symbol,start_date,end_date))            

            count = cursor_all.rowcount            
            pages = round((count / int(limit)), 0)

            l1 = [x[0] for x in rows]
            pagination_d = {'count': count, 'page': page, 'limit': limit, 'pages': pages}            

        except (Exception, psycopg2.DatabaseError) as e:
            error = e
        finally:
            info_d = {'error': error}
            d = {'data': l1, 'pagination': pagination_d, 'info': info_d}
                            
            result = d                
            if conn is not None:
                conn.close()    

        return result


api.add_resource(FinancialData, '/api/financial_data')

# Running the Local Server
if __name__ == '__main__':
    app.run(host='localhost', port=5000)


# http://localhost:5000/api/financial_data?start_date=2023-02-10&end_date=2023-02-20&symbol=IBM&limit=10&page=9

