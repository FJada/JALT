from pymongo import MongoClient

mongo_uri = "mongodb+srv://JadaF:Nipploni@cluster0.9laqhsg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)

db = client['saved_addresses']
collection = db['collections']

# Insert user data into the collection
user_data = [
    {"username": "user1", "addresses": [{"street": "123 Main St", "city": "Cityville", "state": "CA", "zip": "12345"}]},
    {"username": "user2", "addresses": [{"street": "456 Business Blvd", "city": "Worktown", "state": "NY", "zip": "67890"}]},
    # Add more user data as needed
]

collection.insert_many(user_data)

# Verify the creation of the new database and collection
print("Database:", client.list_database_names())
print("Collections in", db.name, ":", db.list_collection_names())
