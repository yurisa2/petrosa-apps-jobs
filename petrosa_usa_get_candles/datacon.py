import datetime
import json
import logging
import os

import newrelic.agent
import pandas as pd
import pymongo
import pytz
import yfinance as yf
from kafka import KafkaProducer

COL_NAME = os.environ.get('COLLECTION_NAME', 'candles_m15')
MINUTES = float(os.environ.get('MINUTES', 15))


@newrelic.agent.background_task()
def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'), 
        readPreference='secondaryPreferred',
        appname='petrosa-nosql-crypto'
    )

    return client


@newrelic.agent.background_task()
def get_data(ticker, period, limit=999999999):

    suffix = period

    client = get_client()
    db = client["petrosa_usa"]
    history = db[COL_NAME]

    results = history.find({'ticker': ticker},
                           sort=[('datetime', -1)]).limit(limit)
    results_list = list(results)

    if (len(results_list) == 0):
        return []

    data_df = pd.DataFrame(results_list)

    data_df = data_df.sort_values("datetime")

    data_df = data_df.rename(columns={"open": "Open",
                                      "high": "High",
                                      "low": "Low",
                                      "close": "Close"}
                             )

    data_df = data_df.set_index('datetime')

    return data_df


@newrelic.agent.background_task()
def get_asset_list():
    client = get_client()
    params = client.petrosa_usa['ticket_list'].find()
    params = list(params)

    return params

def insert_all(k_list):
    client = get_client()
    col = client.petrosa_usa[COL_NAME]
    try:
        col.insert_many(k_list)
    except Exception as e:
        logging.warning(e)


@newrelic.agent.background_task()
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@newrelic.agent.background_task()
def send_all(k_list) -> None:
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_ADDRESS', 'localhost:9093')
    )
    topic = 'usa_candles_hotline'

    for item in k_list:
        item.pop("_id")
        msg = bytes(json.dumps(item, default=json_serial), 'utf-8')
        producer.send(topic, msg)
        

@newrelic.agent.background_task()
def get_ticker_data(symbol: str, k_list: list):
    since = datetime.datetime.now(tz=pytz.timezone(
        'America/New_York')) - datetime.timedelta(minutes=MINUTES)

    try:
        symbol_action = yf.Ticker(symbol)
        hist = symbol_action.history(interval="15m", start=since)
        last_one = hist.iloc[-1].to_dict()
        
        to_send = {}
        to_send['ticker'] = symbol
        to_send['datetime'] = hist.index[-1]
        to_send['open'] = last_one['Open']
        to_send['high'] = last_one['High']
        to_send['low'] = last_one['Low']
        to_send['close'] = last_one['Close']
        to_send['vol'] = last_one['Volume']
        to_send['insert_time'] = datetime.datetime.utcnow()
        k_list.append(to_send)

    except Exception as e:
        logging.error(e)
