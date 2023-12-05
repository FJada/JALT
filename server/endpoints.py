# In endpoints.py
from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz

import data.addresses as addresses
import data.buses as buses  # Importing buses.py
# import data.users as users
# import data.db_connect as dbc Importing db_connect.py as dbc

app = Flask(__name__)
api = Api(app)

# Define the user model
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'home_address': fields.String(required=True, description='Home Address'),
    'work_address': fields.String(required=True, description='Work Address'),
})


DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "MTA Route Planner"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
USERS_EP = '/users'
BUSES_EP = '/bus_routes'
ADDRESSES_EP = '/addresses'
ADDRESS_MENU_EP = '/address_menu'
ADDRESS_MENU_NM = 'Address Menu'
DEL_USER_EP = f'{USERS_EP}/delete'  # Adjusted endpoint for deleting users
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'


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


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'{MAIN_MENU_EP}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {TITLE: MAIN_MENU_NM,
                DEFAULT: 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Users'},  # Updated text
                    '3': {'url': f'{USERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    '4': {'url': '/',
                          'method': 'get', 'text': 'Illustrating a Point!'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{USER_MENU_EP}')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USER_MENU_NM,
                   DEFAULT: '0',
                   'Choices': {
                       '1': {
                            'url': '/',
                            'method': 'get',
                            'text': 'Get User Details',
                       },
                       '0': {
                            'text': 'Return',
                       },
                   },
               }


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: addresses.get_users(),
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
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


@api.route(f'{BUSES_EP}')
class BusRoutes(Resource):
    """
    This class supports fetching details of all available bus routes.
    """
    def get(self):
        """
        This method returns details of all available bus routes.
        """
        return {
            TYPE: DATA,
            TITLE: 'Available Bus Routes',
            DATA: buses.get_bus_routes(),
            MENU: MAIN_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }


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
            print(
                f"Received request: username={username}, "
                f"home_address={home_address}, "
                f"work_address={work_address}"
            )
            # Call the add_user function
            addresses.add_user(username, home_address=home_address, work_address=work_address)

            return {'message': 'User created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


if __name__ == '__main__':
    app.run(debug=True)
