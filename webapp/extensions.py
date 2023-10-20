from pymongo import MongoClient

#instantiate the client separate from the app startup
#make it extensible
mongo_client = MongoClient()
