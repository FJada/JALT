import os
import pymongo as pm
import logging
import certifi as certifi

# Directly specify the absolute path to the error log file
log_file_path = '../server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LOCAL = "0"
CLOUD = "1"

METRO_DB = 'Metro'
client = None
USERS_COLLECTION = 'users'

MONGO_ID = '_id'


def connect_db():
    """
    Connects to the MongoDB database.
    """
    try:
        global client
        print("CONNECTING!!!!")
        if client is None:  # not connected yet!
            print("Setting client because it is None.")
            if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
                print("Connecting to Mongo in the cloud.")
                password = "cluster_pass"
                client = pm.MongoClient(
                    f'mongodb+srv://cluster_user:{password}@cluster0.9laqhsg.mongodb.net/?retryWrites=true&w=majority',
                    tlsCAFile=certifi.where()
                )
            else:
                print("Connecting to Mongo locally.")
                client = pm.MongoClient()
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        raise


def insert_one(collection, doc, db=METRO_DB):
    """
    Insert a single document into the collection.
    """
    try:
        print(f'{db=}')
        return client[db][collection].insert_one(doc)
    except Exception as e:
        logger.error(f"Error inserting document into collection '{collection}': {str(e)}")
        raise


def fetch_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and return the first document found.
    Return None if not found.
    """
    try:
        for doc in client[db][collection].find(filt):
            if MONGO_ID in doc:
                # Convert mongo ID to a string so it works as JSON
                doc[MONGO_ID] = str(doc[MONGO_ID])
            return doc
    except Exception as e:
        logger.error(f"Error fetching document from collection '{collection}': {str(e)}")
        raise


def del_one(collection, filt, db=METRO_DB):
    """
    Find with a filter and delete the first document found.
    """
    try:
        client[db][collection].delete_one(filt)
    except Exception as e:
        logger.error(f"Error deleting document from collection '{collection}': {str(e)}")
        raise


def update_doc(collection, filters, update_dict, db=METRO_DB):
    """
    Update a document in the collection based on filters.
    """
    try:
        return client[db][collection].update_one(filters, {'$set': update_dict})
    except Exception as e:
        logger.error(f"Error updating document in collection '{collection}': {str(e)}")
        raise


def fetch_all(collection, db=METRO_DB):
    """
    Fetch all documents from the collection.
    """
    try:
        ret = []
        for doc in client[db][collection].find():
            ret.append(doc)
        return ret
    except Exception as e:
        logger.error(f"Error fetching all documents from collection '{collection}': {str(e)}")
        raise


def fetch_all_as_dict(key, collection, db=METRO_DB):
    """
    Fetch all documents from the collection and return them as a dictionary.
    """
    try:
        ret = {}
        for doc in client[db][collection].find():
            del doc[MONGO_ID]
            ret[doc[key]] = doc
        return ret
    except Exception as e:
        logger.error(f"Error fetching all documents as dictionary from collection '{collection}': {str(e)}")
        raise
