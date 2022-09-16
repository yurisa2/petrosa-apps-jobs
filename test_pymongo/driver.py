import pymongo
import datetime
import os

client = pymongo.MongoClient(
                                        os.getenv(
                                            'MONGO_URI', 'mongodb://root:wUx3uQRBC8@localhost:27017'),
                                        readPreference='secondaryPreferred',
                                        appname='petrosa-nosql-crypto'
                                        )


msg = {'date_now': datetime.datetime.now()}

client.petrosa_crypto['test_jobs'].insert_one(msg)
