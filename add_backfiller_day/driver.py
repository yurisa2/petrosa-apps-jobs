import requests
import datetime
import pymongo


client = pymongo.MongoClient(
                                        os.getenv(
                                            'MONGO_URI', 'mongodb://root:wUx3uQRBC8@localhost:27017'),
                                        readPreference='secondaryPreferred',
                                        appname='petrosa-nosql-crypto'
                                        )

asset_list_raw = requests.get(
    'https://fapi.binance.com/fapi/v1/ticker/price').json()


periods = ['5m', '15m', '30m', '1h']


start_date = datetime.date.today().isoformat()


item_list = []
for symbol in asset_list_raw:
    for period in periods:
        item = {}
        item['symbol'] = symbol['symbol']
        item['day'] = start_date
        item['period'] = period
        item['state'] = 0
        item['checked'] = False
        item_list.append(item)

print(len(item_list))


db = client.petrosa_crypto
collection = db['backfill']

collection.insert_many(item_list)
