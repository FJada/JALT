from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-mta-data/<account_number>')
def get_mta_data(account_number):
    mta_data = {"account_number": "12345",
        "addresses": [
            {
                "name": "home",
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "train_station": "Penn Station",
                "bus_station": "Port Authority Bus Terminal"
            }}
    extra = request.args.get("extra")
    if extra:
        mta_data["extra"] = extra
    
    return jsonify(mta_data)

if __name__ == '__main__':
    app.run(debug=True)
