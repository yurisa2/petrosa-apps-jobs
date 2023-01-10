from kafka import KafkaProducer
import datetime
import logging
import os
import random
import datetime
import json


import pandas as pd
import pymongo
import newrelic


def get_client() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-nosql-crypto'
    )

    return client


def get_data(ticker, period, limit=999999999):

    suffix = period

    client = get_client()
    db = client["petrosa_usa"]
    history = db["candles_" + suffix]

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


def get_asset_list():
    client = get_client()
    params = client.petrosa_usa['ticket_list'].find()
    params = list(params)

    return params

def insert_all(k_list):
    client = get_client()
    # col = client.petrosa_usa[os.environ.get('CANDLE_COLLECTION')]
    col = client.petrosa_usa['candles_m15']
    try:
        col.insert_many(k_list)
    except Exception as e:
        logging.warning(e)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def send_all(k_list) -> None:
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_ADDRESS', 'localhost:9093')
    )
    topic = 'usa_candles_hotline'

    for item in k_list:
        item.pop("_id")
        msg = json.dumps(item, default=json_serial)
        producer.send(topic, msg)