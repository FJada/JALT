# """
# This is the file with some of the endpoints for our flask app
# The endpoint called `endpoints` will return all available endpoints.

# """
# from flask import Flask
# from flask_restx import Resource, Api

# app = Flask(__name__)
# api = Api(app)

# from flask import Flask, jsonify, request
# from flask_restx import Resource, Api
# import requests

# app = Flask(__name__)
# api = Api(app)

# MTA_API_BASE_URL_ACE = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
# MTA_API_KEY = "KBf8CHIirk2T8svAwIqS68ZtrnJQ5pypIrLuluUh" 

# # Set up the request headers with the API key
# headers = {"x-api-key": MTA_API_KEY}

# @api.route('/endpoints')
# class Endpoints(Resource):
#     """
#     This class will serve as live, fetchable documentation of what endpoints
#     are available in the system.
#     """
#     def get(self):
#         """
#         The `get()` method will return a list of available endpoints.
#         """
#         endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
#         return {"Available endpoints": endpoints}
    
# # Endpoint to get subway line data for group
# @api.route('/subway-lines')
# class SubwayLines_ACE(Resource):
#     def get(self):
#         try:
#             # Make a request to the MTA API to get subway line data
#             response = requests.get(f"{MTA_API_BASE_URL}/subway/lines", headers=headers)

#             if response.status_code == 200:
#                 subway_lines = response.json()
#                 return {"subway_lines": subway_lines}
#             else:
#                 return {"error": "Failed to fetch subway lines"}, response.status_code

#         except Exception as e:
#             return {"error": str(e)}, 500

# # Endpoint to get details of a specific subway line in the ACE group
# @api.route('/subway-lines/<line_id>')
# class SubwayLineDetails_ACE(Resource):
#     def get(self, line_id):
#         try:
#             # Make a request to the MTA API to get details of a specific subway line
#             response = requests.get(f"{MTA_API_BASE_URL}/subway/lines/{line_id}", headers=headers)

#             if response.status_code == 200:
#                 subway_line = response.json()
#                 return {"subway_line": subway_line}
#             else:
#                 return {"error": "Failed to fetch subway line details"}, response.status_code

#         except Exception as e:
#             return {"error": str(e)}, 500

# if __name__ == '__main__':
#     app.run(debug=True)
