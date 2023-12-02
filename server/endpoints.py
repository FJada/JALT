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

@api.route('/add_user')
class AddUser(Resource):
    """
    Adds a new user with a username.
    """
    @api.expect(addresses.USER_MODEL)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        username = request.json[addresses.USERNAME]
        account_id = request.json[addresses.ACCOUNT_ID]
        home_address = request.json[addresses.ADDRESSES][addresses.HOME]
        work_address = request.json[addresses.ADDRESSES][addresses.WORK]

        try:
            addresses.add_user(username, account_id, home_address, work_address)
            return {addresses.USERNAME: username, 'Added': True}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

@api.route('/add_address/<username>')
class AddAddress(Resource):
    """
    Adds a new address to a user.
    """
    @api.expect(addresses.ADDRESS_MODEL)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self, username):
        """
        Add an address to a user.
        """
        address_type = request.json[addresses.ADDRESS]
        address_value = request.json[addresses.ADDRESSES][address_type]

        try:
            addresses.add_address(username, address_type, address_value)
            return {addresses.ADDRESS: address_type, 'Added to': username}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
