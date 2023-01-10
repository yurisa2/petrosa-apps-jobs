import datetime
import logging
import os
import threading
import time

import pytz
import yfinance as yf

import datacon



def get_ticker_data(symbol: str, k_list: list):
    try:
        symbol_action = yf.Ticker(symbol)
        hist = symbol_action.history(interval="15m", start=since)
        last_one = hist.iloc[-1].to_dict()
        last_one['symbol'] = symbol
        last_one['datetime'] = hist.index[-1]
        k_list.append(last_one)
        
    except Exception as e:
        logging.error(e)

since = datetime.datetime.now(tz=pytz.timezone('America/New_York')) - datetime.timedelta(hours=15)
list_assets = datacon.get_asset_list()

thread_list = []
candle_list = []

for item in list_assets:
    thread_ = threading.Thread(
        target=get_ticker_data, args=(item['Symbol'], candle_list,)
        )
    thread_list.append(thread_)
    thread_.start()
    time.sleep(0.1)
    

for thread_o in thread_list:
    thread_o.join()
    
datacon.insert_all(candle_list)
datacon.send_all(candle_list)
