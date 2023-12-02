# In endpoints.py
from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
from data import addresses

app = Flask(__name__)
api = Api(app)

# Define the user model
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'home_address': fields.String(required=True, description='Home Address'),
    'work_address': fields.String(required=True, description='Work Address'),
})

DELETE = 'delete'
DEFAULT = 'Default'
ADDRESS_MENU_EP = '/address_menu'
ADDRESS_MENU_NM = 'Address Menu'
ADDRESSES_EP = '/addresses'
DEL_USER_EP = f'{ADDRESSES_EP}/{DELETE}'


@api.route(f'{ADDRESSES_EP}')
class Addresses(Resource):
    """
    This class supports fetching a list of all addresses.
    """
    def get(self):
        """
        This method returns all addresses.
        """
        # Fetch the latest user data from the database
        users_data = addresses.get_all_users()

        return {
            addresses.USERNAME: [user.get(addresses.USERNAME) for user in users_data],
            addresses.ACCOUNT_ID: [user.get(addresses.ACCOUNT_ID) for user in users_data],
            addresses.ADDRESSES: [user.get(addresses.ADDRESSES, {}) for user in users_data],
        }


@api.route(f'{DEL_USER_EP}/<username>')
class DelUser(Resource):
    """
    Deletes a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, username):
        """
        Deletes a user by username.
        """
        try:
            addresses.del_user(username)
            return {username: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
            

# Add a new endpoint for adding a user with both home and work addresses
@api.route('/add_user')
class AddUser(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(user_model)
    def post(self):
        """
        Adds a new user.
        """
        try:
            # Print received parameters for debugging
            data = request.json
            username = data.get('username')
            home_address = data.get('home_address')
            work_address = data.get('work_address')
            print(f"Received request: username={username}, home_address={home_address}, work_address={work_address}")

            # Call the add_user function
            addresses.add_user(username, home_address=home_address, work_address=work_address)

            return {'message': 'User created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

if __name__ == '__main__':
    app.run(debug=True)
