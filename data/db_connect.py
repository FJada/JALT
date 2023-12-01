import os
import pymongo as pm

LOCAL = "0"
CLOUD = "1"

METRO_DB = 'Metro'

client = None

MONGO_ID = '_id'


def connect_db():
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            username = 'af3842'
            password = 'af3842'
            cluster_hostname = 'cluster0.9laqhsg.mongodb.net'

            if not (username and password and cluster_hostname):
                raise ValueError('You must set your username, password, '
                                 + 'and cluster hostname to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://{username}:{password}@{cluster_hostname}/?retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=METRO_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=METRO_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=METRO_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
