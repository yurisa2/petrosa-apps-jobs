import datetime
import pymongo
import os
import logging

client = pymongo.MongoClient(
                            os.getenv(
                                'MONGO_URI', 'mongodb://root:QnjfRW7nl6@localhost:27017'),
                            readPreference='secondaryPreferred',
                            appname='petrosa-nosql-crypto'
                            )

periods = ['5m', '15m', '30m', '1h']

socket_period_table = 'candles_h1'
socket_period = 1
socket_time = datetime.datetime.now() - datetime.timedelta(days=socket_period)

asset_list_raw_table = client.petrosa_crypto[socket_period_table]
asset_list_raw_list=asset_list_raw_table.find({"datetime": {"$gte": socket_time}, "origin": 'socket'})

symbols_last_period = []

for item in asset_list_raw_list:
    symbols_last_period.append(item['ticker'])

symbols_last_period = list(dict.fromkeys(symbols_last_period))

print(symbols_last_period)

# days_prior = 700

# days_list = []

# for _ in range(1, days_prior):
#     start_date = (datetime.date.today()
#                   - datetime.timedelta(days=_)).isoformat()
#     days_list.append(start_date)

# item_list = []
# for symbol in symbols_last_period:
#     for day_item in days_list:
#         for period in periods:
#             item = {}
#             item['symbol'] = symbol
#             item['day'] = day_item
#             item['period'] = period
#             item_list.append(item)



# update_list_commands = []

# base_item = {}
# base_item['state'] = 0
# base_item['checked'] = False
# base_item['petrosa_timestamp'] = datetime.datetime.now()

# for item in item_list:
#     cmm = pymongo.UpdateOne(item, {
# 	  "$setOnInsert": {**item, **base_item}
# 	 }, upsert=True)

#     update_list_commands.append(cmm)

# db = client.petrosa_crypto
# collection = db['backfill']

# collection.bulk_write(update_list_commands)

db.candles_h1.deleteMany({"ticker": {"$nin": ['ETHUSDT', 'BTCUSDT', 'NEOUSDT', 'LTCUSDT', 'IOTAUSDT', 'XLMUSDT', 'BNBUSDT', 'XRPUSDT', 'VETUSDT', 'OMGUSDT', 'QTUMUSDT', 'ETCUSDT', 'ICXUSDT', 'ZRXUSDT', 'IOSTUSDT', 'DASHUSDT', 'THETAUSDT', 'ADAUSDT', 'EOSUSDT', 'FTMUSDT', 'DOGEUSDT', 'DUSKUSDT', 'MTLUSDT', 'TOMOUSDT', 'DENTUSDT', 'MATICUSDT', 'ALGOUSDT', 'TRXUSDT', 'WAVESUSDT', 'HOTUSDT', 'ONTUSDT', 'LINKUSDT', 'ZILUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'CELRUSDT', 'CHZUSDT', 'RENUSDT', 'NKNUSDT', 'LTCBUSD', 'LINKBUSD', 'IOTXUSDT', 'BCHUSDT', 'BNBBUSD', 'BTCBUSD', 'RVNUSDT', 'HBARUSDT', 'XRPBUSD', 'TRXBUSD', 'ENJUSDT', 'ATOMUSDT', 'BTSUSDT', 'ONEUSDT', 'ANKRUSDT', 'CHRUSDT', 'MATICBUSD', 'SOLUSDT', 'SOLBUSD', 'STMXUSDT', 'XTZUSDT', 'ETHBUSD', 'ETCBUSD', 'KAVAUSDT', 'ARPAUSDT', 'RLCUSDT', 'BANDUSDT', 'ADABUSD', 'DOGEBUSD', 'MANAUSDT', 'BALUSDT', 'OGNUSDT', 'WAVESBUSD', 'KNCUSDT', 'LRCUSDT', 'COMPUSDT', 'ZENUSDT', 'CTSIUSDT', 'COTIUSDT', 'STORJUSDT', 'CRVUSDT', 'DOTUSDT', 'MKRUSDT', 'SCUSDT', 'SNXUSDT', 'DGBUSDT', 'SXPUSDT', 'SANDUSDT', 'SANDBUSD', 'RSRUSDT', 'SUSHIUSDT', 'KSMUSDT', 'YFIUSDT', 'UNIUSDT', 'BLZUSDT', 'ANTUSDT', 'AAVEUSDT', 'NEARBUSD', 'AUDIOUSDT', 'ALPHAUSDT', 'FILUSDT', 'CTKUSDT', 'OCEANUSDT', 'DOTBUSD', 'TRBUSDT', '1INCHUSDT', 'AVAXUSDT', 'EGLDUSDT', 'RUNEUSDT', 'BELUSDT', 'UNIBUSD', 'AVAXBUSD', 'FLMUSDT', 'LITUSDT', 'SFPUSDT', 'ALICEUSDT', 'NEARUSDT', 'FILBUSD', 'DODOBUSD', 'INJUSDT', 'TLMUSDT', 'ROSEUSDT', 'XEMUSDT', 'AXSUSDT', 'UNFIUSDT', 'SKLUSDT', 'BAKEUSDT', 'FTMBUSD', 'ATAUSDT', 'MASKUSDT', 'GRTUSDT', 'CELOUSDT', 'REEFUSDT', 'QNTUSDT', 'AUCTIONBUSD', 'LINAUSDT', 'GALAUSDT', 'BNXUSDT', 'TLMBUSD', 'ICPBUSD', 'ICPUSDT', 'LPTUSDT', 'GTCUSDT', 'ARUSDT', 'API3USDT', 'FTTBUSD', 'KLAYUSDT', 'C98USDT', 'PEOPLEUSDT', 'IMXUSDT', 'WOOUSDT', 'RAYUSDT', 'GMTUSDT', 'APEBUSD', 'FLOWUSDT', 'GALUSDT', 'DYDXUSDT', 'GALABUSD', 'APTUSDT', 'DARUSDT', 'AMBBUSD', 'APTBUSD', 'JASMYUSDT', 'ENSUSDT', 'CVXBUSD', 'CVXUSDT', 'SPELLUSDT', 'ANCBUSD', 'GMTBUSD', 'APEUSDT', 'GALBUSD', 'LDOBUSD', 'LDOUSDT', 'STGUSDT', 'OPUSDT', 'LEVERBUSD', 'PHBBUSD']}})
