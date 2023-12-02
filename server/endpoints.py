from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
from data import addresses

app = Flask(__name__)
api = Api(app)

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
        return {
            addresses.USERNAME: addresses.USERNAME,
            addresses.ACCOUNT_ID: addresses.ACCOUNT_ID,
            addresses.ADDRESSES: addresses.ADDRESSES,
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
    """
    Adds a new user.
    """
    @api.response(HTTPStatus.CREATED, 'User Created Successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.doc(params={
        'username': 'Username of the new user',
        'home_address': 'Home address of the new user',
        'work_address': 'Work address of the new user'
    })
    def post(self):
        """
        Adds a new user.
        """
        try:
            # Extract user information from the form parameters
            username = request.form.get('username')
            home_address = request.form.get('home_address')
            work_address = request.form.get('work_address')

            # Add the user with username, home address, and work address
            addresses.add_user(username, account_id=None, home_address=home_address, work_address=work_address)

            return {'message': 'User created successfully'}, HTTPStatus.CREATED
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
