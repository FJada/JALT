import os
import pymongo
from flask_restx import Api

LOCAL = "0"
CLOUD = "1"
METRO_DB = 'Metro'
client = None

MONGO_ID = '_id'

api = Api()


def connect_db():
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            username = 'cluster_user'
            password = 'cluster_pass'
            cluster_hostname = 'cluster0.9laqhsg.mongodb.net'
            if not (username and password and cluster_hostname):
                raise ValueError('You must set your username, password, '
                                 + 'and cluster hostname to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pymongo.MongoClient(f'mongodb+srv://{username}:{password}@{cluster_hostname}/?retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pymongo.MongoClient()


def get_collection(collection_name, db=METRO_DB):
    connect_db()
    return client[db][collection_name]


def insert_one(collection, doc, db=METRO_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{collection.db=}')
    return collection.insert_one(doc)


def fetch_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and return on the first doc found.
    """
    doc = collection.find_one(filt)
    if doc and MONGO_ID in doc:
        # Convert mongo ID to a string so it works as JSON
        doc[MONGO_ID] = str(doc[MONGO_ID])
    return doc


def del_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and return on the first doc found.
    """
    connect_db()  # Ensure the connection is established
    get_collection(collection, db).delete_one(filt)


def fetch_all(collection_name, db=METRO_DB):
    connect_db()
    collection = client[db][collection_name]
    ret = []
    for doc in collection.find({}):
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=METRO_DB):
    ret = {}
    for doc in collection.find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
