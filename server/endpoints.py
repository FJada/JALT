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
ADD_USER_EP = f'{ADDRESSES_EP}/add_user'
ADD_ADDRESS_EP = f'{ADDRESSES_EP}/add_address'

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

@api.route(ADD_USER_EP)
class AddUser(Resource):
    """
    Adds a new user with a given username and addresses.
    """
    @api.expect(addresses.USER_MODEL)
    @api.response(HTTPStatus.CREATED, 'User Created')
    @api.response(HTTPStatus.CONFLICT, 'User Already Exists')
    def post(self):
        """
        Adds a new user with a given username and addresses.
        """
        data = request.json
        username = data.get(addresses.USERNAME)
        account_id = data.get(addresses.ACCOUNT_ID)
        home_address = data.get(addresses.HOME)
        work_address = data.get(addresses.WORK)

        try:
            addresses.add_user(username, account_id, home_address, work_address)
            return {addresses.USERNAME: username, 'status': 'User Created'}, HTTPStatus.CREATED
        except ValueError as e:
            raise wz.Conflict(f'{str(e)}')

@api.route(ADD_ADDRESS_EP)
class AddAddress(Resource):
    """
    Adds a new address to an existing user based on the username.
    """
    @api.expect(addresses.ADDRESS_MODEL)
    @api.response(HTTPStatus.CREATED, 'Address Added')
    @api.response(HTTPStatus.NOT_FOUND, 'User Not Found')
    def post(self):
        """
        Adds a new address to an existing user based on the username.
        """
