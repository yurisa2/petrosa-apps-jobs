import requests
import datetime
import pymongo
import os

client = pymongo.MongoClient(
                            os.getenv(
                                'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
                            readPreference='secondaryPreferred',
                            appname='petrosa-nosql-crypto'
                            )

asset_list_raw = requests.get(
    'https://fapi.binance.com/fapi/v1/ticker/price').json()


periods = ['5m', '15m', '30m', '1h']

days_prior = 700


days_list = []

for _ in range(1, days_prior):
    start_date = (datetime.date.today()
                  - datetime.timedelta(days=_)).isoformat()
    days_list.append(start_date)

item_list = []
for symbol in asset_list_raw:
    for day_item in days_list:
        for period in periods:
            item = {}
            item['symbol'] = symbol['symbol']
            item['day'] = day_item
            item['period'] = period
            item_list.append(item)


print(len(item_list))


update_list_commands = []

base_item = {}
base_item['state'] = 0
base_item['checked'] = False
base_item['petrosa_timestamp'] = datetime.datetime.now()

for item in item_list:
    cmm = pymongo.UpdateOne(item, {
	  "$setOnInsert": {**item, **base_item}
	 }, upsert=True)

    update_list_commands.append(cmm)

db = client.petrosa_crypto
collection = db['backfill']

collection.bulk_write(update_list_commands)
