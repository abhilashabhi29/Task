#!/usr/bin/python3
from flask import Flask, request, jsonify,render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
import os

# import custom functions
# from UrlCreation import create_url_pattern
# from download import csv_download
# from extract_data import push_df_to_db

from db_settings import Settings
from download import Download
from extract_data import  ExtraData
from url_creation import UrlCreation


db_connect = create_engine('sqlite:///demo.db')
app = Flask(__name__)
api = Api(app)


class Stock_Details(Resource):
    @app.route('/Stock_Details')
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from users") # This line performs query and returns json result
        d = {'stock': [i[:] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
        return jsonify(d)

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        'SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TIMESTAMP'
        SYMBOL = request.json['SYMBOL']
        SERIES = request.json['SERIES']
        OPEN = request.json['OPEN']
        HIGH = request.json['HIGH']
        LOW = request.json['LOW']
        CLOSE = request.json['CLOSE']
        LAST = request.json['LAST']
        PREVCLOSE = request.json['PREVCLOSE']
        TOTTRDQTY = request.json['TOTTRDQTY']
        TIMESTAMP = request.json['TIMESTAMP']

        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(SYMBOL,SERIES,OPEN,
                             HIGH, LOW, CLOSE, LAST,
                             PREVCLOSE, TOTTRDQTY, TIMESTAMP))
        return {'status':'success'}

    @app.route('/Stock_Details/<username>')
    def Symbol_Stock_Detailse(username):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from users where SYMBOL= ?",[username]) # This line performs query and returns json result

        d = {'stock': [i[:] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
        r = json.dumps(d)
        return r

    @app.route('/Symbols')
    def Symbols():
        conn = db_connect.connect() # connect to database
        query = conn.execute("select DISTINCT SYMBOL from users")

        d = [i[0] for i in query.cursor.fetchall()]
        print d
        r = json.dumps(d)
        return r




    @app.route('/')
    def index():
        return render_template('index.html')


if __name__ == '__main__':
    extract_data = ExtraData()
    downloads = Download()
    settings = Settings()
    url_creation = UrlCreation()

    db = "demo.db"
    current_url = "https://archives.nseindia.com/content/historical/EQUITIES/2020/FEB/cm06FEB2020bhav.csv.zip"
    working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    urls = url_creation.create_url_pattern(current_url,working_days)
    path = os.getcwd()
    download = downloads.csv_download(urls,path)

    conn = settings.create_connection(db)
    table = settings.create_table(conn)

    if download:
        conn = extract_data.push_df_to_db(conn,table)

    app.run()
