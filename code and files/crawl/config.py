import pymongo

# MongoDb

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
DB_NAME = 'IEA'

#  mongodb Host, collection
Client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
iea = Client[DB_NAME]["iea"]
policy = Client[DB_NAME]["policy"]
all_policy = Client[DB_NAME]["all_policy"]