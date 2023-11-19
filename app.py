from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = "mongodb+srv://af3842:Nipploni1!@cluster0.9laqhsg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

db = client.collections

# Sample route to retrieve user addresses
@app.route('/user/<username>/addresses', methods=['GET'])
def get_user_addresses(username):
    user = db.users.find_one({"username": username})
    if user:
        addresses = user.get('addresses', [])
        return jsonify({"addresses": addresses})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
