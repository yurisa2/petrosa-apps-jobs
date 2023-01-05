import os
import datetime
import logging
import pymongo
import pytz
import newrelic.agent


@newrelic.agent.background_task()
def get_client():
    client = pymongo.MongoClient(
        os.getenv(
            'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
        readPreference='secondaryPreferred',
        appname='petrosa-nosql-crypto'
    )
    
    return client


@newrelic.agent.background_task()
def write_bulk_list(update_list_commands):
    db = get_client().petrosa_crypto
    collection = db['backfill']
    logging.warning('Writing to mongo... NOW')
    collection.bulk_write(update_list_commands)

    return True


@newrelic.agent.background_task()
def generate_update_commands(item_list):
    update_list_commands = []

    base_item = {}
    base_item['state'] = 0
    base_item['checked'] = False
    base_item['petrosa_timestamp'] = datetime.datetime.now(tz=pytz.utc)

    logging.warning('Creating DB commands')
    for item in item_list:
        cmm = pymongo.UpdateOne(item, {
            "$setOnInsert": {**item, **base_item}
        }, upsert=True)

        update_list_commands.append(cmm)

    return update_list_commands


periods = ['5m', '15m', '30m', '1h']

days_prior = 700

socket_period_table = 'candles_h1'
socket_period = 1
socket_time = datetime.datetime.now(
    tz=pytz.utc) - datetime.timedelta(days=socket_period)

logging.warning('Connecting to db to look for socket updates in the last socket_period')
asset_list_raw_table = get_client().petrosa_crypto[socket_period_table]
symbols_last_period = []
asset_list_raw_list = asset_list_raw_table.find(
    {"datetime": {"$gte": socket_time}, "origin": 'socket'})
symbols_last_period = list(dict.fromkeys(symbols_last_period))

logging.warning(str(len(symbols_last_period)) +
                ' unique tickers from sokec on the last socket_period')


for item in asset_list_raw_list:
    symbols_last_period.append(item['ticker'])


days_list = []

for _ in range(1, days_prior):
    start_date = (datetime.date.today()
                  - datetime.timedelta(days=_)).isoformat()
    days_list.append(start_date)

item_list = []
for symbol in symbols_last_period:
    for day_item in days_list:
        for period in periods:
            item = {}
            item['symbol'] = symbol
            item['day'] = day_item
            item['period'] = period
            item_list.append(item)

logging.warning('Size of the long tail: ' + str(len(item_list)))


update_list = generate_update_commands(item_list)
write_bulk_list(update_list)

logging.warning('Bye')
