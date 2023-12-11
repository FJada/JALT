import os
import pymongo as pm
from flask_restx import Api

LOCAL = "0"
CLOUD = "1"
METRO_DB = 'Metro'
client = None

MONGO_ID = '_id'

api = Api()

def connect_db():
    print("CONNECTING!!!!")
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = cluster_pass
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://cluster_user:{password}'
                                    + '@cluster0.9laqhsg.mongodb.net/'
                                    + '?retryWrites=true&w=majority')

        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=RECIPE_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, fields=None, db=RECIPE_DB):
    """
    Find with a filter and return on the first doc found.
    """

    res = client[db][collection].find(filt, fields)
    print(f'{res=}')
    if res is not None:
        for doc in res:
            if MONGO_ID in doc:
                # Convert mongo ID to a string so it works as JSON
                doc[MONGO_ID] = str(doc[MONGO_ID])
            return doc

    raise ValueError("Object to fetch does not exist")


def del_one(collection, filt, db=RECIPE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=RECIPE_DB):
    ret = []
    res = client[db][collection].find()
    if res is not None:
        for doc in res:
            ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=RECIPE_DB):
    ret = {}
    res = client[db][collection].find()
    if res is not None:
        for doc in res:
            del doc[MONGO_ID]
            ret[doc[key]] = doc
    return ret


def update_one(collection, filter, query, db=RECIPE_DB):
    return client[db][collection].update_one(filter, query)
