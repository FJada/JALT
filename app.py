from pymongo import MongoClient

mongo_uri = "mongodb+srv://JadaF:Nipploni@cluster0.9laqhsg.mongodb.net/saved_addresses?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)

db = client['saved_addresses']
collection = db['collections']

user_data = [
    {
        "account_number": "12345",
        "addresses": [
            {
                "name": "home",
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "train_station": "Penn Station",
                "bus_station": "Port Authority Bus Terminal"
            },
            {
                "name": "work",
                "street": "456 Business Blvd",
                "city": "Brooklyn",
                "state": "NY",
                "zip": "11201",
                "train_station": "Atlantic Terminal",
                "bus_station": "Jay Street-MetroTech Bus Station"
            }
        ]
    },
    {
        "account_number": "67890",
        "addresses": [
            {
                "name": "home",
                "street": "789 Residence Ln",
                "city": "Queens",
                "state": "NY",
                "zip": "11354",
                "train_station": "Flushing-Main Street Station",
                "bus_station": "Queensboro Plaza Bus Terminal"
            },
            {
                "name": "favorite bar",
                "street": "321 Cheers St",
                "city": "Manhattan",
                "state": "NY",
                "zip": "10021",
                "train_station": "Grand Central Terminal",
                "bus_station": "East Side Bus Terminal"
            }
        ]
    },
    # Add more user data as needed
]

collection.insert_many(user_data)

# Verify the creation of the new database and collection
print("Database:", client.list_database_names())
print("Collections in", db.name, ":", db.list_collection_names())
