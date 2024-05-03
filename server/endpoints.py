from http import HTTPStatus
from flask import Flask, request, send_file
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
import data.users as us
import data.routes as routes
import data.buses as buses
import data.trains as trains
import logging
import data.form as form
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

DEFAULT = 'Default'
MENU = 'menu'
ENDPOINTS_EP = '/endpoints'
OPEN_ENDPOINTS = "Currently available endpoints"
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "MTA Route Planner"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
USERS_EP = '/users'
BUSES_EP = '/bus_routes'
TRAINS_EP = '/train_routes'
ADDRESSES_EP = '/addresses'
ADDRESS_MENU_EP = '/address_menu'
ADDRESS_MENU_NM = 'Address Menu'
DEL_USER_EP = f'{USERS_EP}/delete'  # Adjusted endpoint for deleting users
LOGIN_USER_EP = '/users/login'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
HOME_ADDR_EP = '/home_address'
ROUTE_EP = '/routes'
# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'account_id': fields.String(required=True, description='Account ID'),
    'password': fields.String(required=True, description='Password'),

})

add_home_address_model = api.model('AddHomeAddress', {
    'username': fields.String(required=True, description='Username'),
    'home_address': fields.String(required=True, description='Home Address'),
})

route_model = api.model('Route', {
    'starting_point': fields.String(required=True, description='Starting Point'),
    'ending_point': fields.String(required=True, description='Ending Point'),
})

get_account_id_model = api.model('GetAccountID', {
    'username': fields.String(required=True, description='Username'),
    'account_id': fields.String(description='Account ID'),
})

bus_model = api.model('Bus', {
    'bus_name': fields.String(required=True, description='Bus Name'),
    'borough': fields.String(required=True, description='Borough Name'),
    'favorite': fields.Boolean(description='Favorite', default=False),
})

train_model = api.model('Train', {
    'train_name': fields.String(required=True, description='Train Name'),
    'vehicle_id': fields.String(required=True, description='Vehicle ID'),
    'favorite': fields.Boolean(description='Favorite', default=False),
})


@api.route('/errorlog')
class ErrorLog(Resource):
    """
    This class allows retrieval of the error log file.
    """
    def get(self):
        """
        Retrieves and returns the content of the error log file.
        """
        try:
            # Use send_file to return the error log file
            return send_file('error.log', mimetype='text/plain')
        except FileNotFoundError:
            api.abort(HTTPStatus.NOT_FOUND, "Error log file not found")


@api.route('/hello')
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
        return {'hello': 'world'}


@api.route('/addresses')
class Addresses(Resource):
    """
    This class supports fetching a list of all addresses.
    """
    def get(self):
        """
        This method returns all addresses.
        """
        # Fetch the latest user data from the database
        users_data = us.get_users_as_dict()

        return {
            us.HOME: [user.get(us.HOME, '') for user in users_data],
        }


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
        return {OPEN_ENDPOINTS: endpoints}


@api.route('/MainMenu')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {TITLE: 'MTA Route Planner',
                RETURN: '/users'}


@api.route('/user_menu')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
            TITLE: 'User Menu',
            RETURN: '/MainMenu',
        }


@api.route('/users')
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
            DATA: us.get_users_as_dict(),
            RETURN: '/MainMenu',
        }


@api.route('/users/<username>')
class GetUserByUsername(Resource):
    """
    Gets a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, username):
        """
        Gets a user by username.
        """
        try:
            user = us.get_user_by_username(username)
            if user:
                return {
                    TYPE: DATA,
                    TITLE: f'User Details for {username}',
                    DATA: user,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'User with username {username} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/users/delete/<username>')
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
            us.del_user(username, True)
            return {username: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


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
            print(f"Received request: username={username}")
            # Call the add_user function
            account_id = us.gen_account_id()
            password = us.gen_password()
            us.add_user(username, account_id, password)

            return {'message': 'User created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/users/account/<account_id>')
class GetUserByAccountId(Resource):
    """
    Gets a user by account ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, account_id):
        """
        Gets a user by account ID.
        """
        try:
            user = us.get_user_by_account_id(account_id)
            if user:
                return {
                    TYPE: DATA,
                    TITLE: f'User Details for Account ID {account_id}',
                    DATA: user,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'User with account ID {account_id} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/users/account/<password>')
class GetUserByPassword(Resource):
    """
    Gets a user by password
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, password):
        """
        Gets a user by password.
        """
        try:
            user = us.get_user_by_password(password)
            if user:
                return {
                    TYPE: DATA,
                    TITLE: f'User Details for Account ID {password}',
                    DATA: user,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'User with account ID {password} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/users/login')
class Login(Resource):
    """
    Log in a user using username or account ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(user_model)  # Modify the model to accept both username and account ID
    def post(self):
        """
        Log in a user using username or account ID.
        """
        try:
            data = request.json
            username = data.get('username')
            account_id = data.get('account_id')
            password = data.get('password')
            if username:
                user = us.get_user_by_username(username)
            elif account_id:
                user = us.get_user_by_account_id(account_id)
            elif password:
                user = us.get_user_by_password(password)
            else:
                raise ValueError("Username, account ID, and password are missing.")
            if user:
                return {
                    TYPE: DATA,
                    TITLE: f'User Details for {username}, Account ID {account_id} and password {password}',
                    DATA: user,
                    RETURN: '/MainMenu',
                }, HTTPStatus.OK
            else:
                raise wz.NotFound("User not found.")
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/users/home_address')
class AddHomeAddress(Resource):
    """
    Adds a home address to a user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(add_home_address_model)  # Use the same modified model for this endpoint
    def post(self):
        """
        Adds a home address to a user.
        """
        try:
            # Get data from the request
            data = request.json
            username = data.get('username')
            home_address = data.get('home_address')

            # Call the add_home_address function
            us.add_home_address(username, home_address)

            return {'message': 'Home address added successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/users/home_address/<username>')
class GetHomeAddress(Resource):
    """
    Gets the home address of a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, username):
        """
        Gets the home address of a user by username.
        """
        try:
            user = us.get_user_by_username(username)
            if user:
                home_address = us.get_home_address(user)
                return {
                    TYPE: DATA,
                    TITLE: f'Home Address for {username}',
                    DATA: {'home_address': home_address},
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'User with username {username} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/add_route')
class AddRoute(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(route_model)
    def post(self):
        """
        Adds a new route.
        """
        try:
            # Print received parameters for debugging
            data = request.json
            starting_point = data.get('starting_point')
            ending_point = data.get('ending_point')
            print(f"Received request: starting_point={starting_point}, ending_point={ending_point}")
            # Call the add_route function
            route_id = routes.gen_route_id()
            routes.add_route(starting_point, ending_point, route_id)

            return {'message': 'Route created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/routes')
class Routes(Resource):
    """
    This class supports fetching a list of all routes.
    """
    def get(self):
        """
        This method returns all routes.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Routes',
            DATA: routes.get_routes_as_dict(),
            RETURN: '/MainMenu',
        }


@api.route('/routes/<route_id>')
class GetRouteById(Resource):
    """
    Gets a route by route ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, route_id):
        """
        Gets a route by route ID.
        """
        try:
            route = routes.get_route_by_route_id(route_id)
            if route:
                return {
                    TYPE: DATA,
                    TITLE: f'Route Details for Route ID {route_id}',
                    DATA: route,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'Route with route ID {route_id} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/routes/delete/<route_id>')
class DelRoute(Resource):
    """
    Deletes a route by route ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, route_id):
        """
        Deletes a route by route ID.
        """
        try:
            routes.del_route(route_id)
            return {route_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/users/account_id')
class GetAccountID(Resource):
    """
    Gets the account ID of a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(get_account_id_model)
    def get(self):
        """
        Gets the account ID of a user by username.
        """
        try:
            # Get data from the request
            data = request.json
            username = data.get('username')

            # Call the get_account_id function
            account_id = us.get_account_id(username)

            if account_id:
                return {'account_id': account_id}
            else:
                raise wz.NotFound(f'User with username {username} not found.')
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/trains')
class Trains(Resource):
    """
    This class supports fetching a list of all trains.
    """
    def get(self):
        """
        This method returns all trains.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current trains',
            DATA: trains.get_trains_as_dict(),
            RETURN: '/MainMenu',
        }


@api.route('/trains/add_train')
class AddTrain(Resource):
    """
    Adds a new train.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(train_model)  # Create a model for the train data
    def post(self):
        """
        Adds a new train.
        """
        try:
            data = request.json
            train_name = data.get('train_name')
            vehicle_id = data.get('vehicle_id')
            favorite = data.get('favorite', False)

            # Call the add_bus function
            trains.add_train(train_name, vehicle_id, favorite)

            return {'message': 'Train created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/trains/delete_train/<train_name>')
class DelTrain(Resource):
    """
    Deletes a train by train name
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def delete(self, train_name):
        """
        Deletes a train by train name
        """
        try:
            trains.del_train(train_name, True)
            return {train_name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/trains/<train_name>')
class GetTrainByTrainName(Resource):
    """
    Gets a train by train name
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, train_name):
        """
        Gets a train by train name
        """
        try:
            train = trains.get_train_by_train_name(train_name)
            if trains:
                return {
                    TYPE: DATA,
                    TITLE: f'Train Details for {train_name}',
                    DATA: train,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'train with name {train_name} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/buses')
class Buses(Resource):
    """
    This class supports fetching a list of all buses.
    """
    def get(self):
        """
        This method returns all buses.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current buses',
            DATA: buses.get_buses_as_dict(),
            RETURN: '/MainMenu',
            }


@api.route('/buses/<bus_name>')
class GetBusByBusName(Resource):
    """
    Gets a bus by bus name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, bus_name):
        """
        Gets a bus by bus name.
        """
        try:
            bus = buses.get_bus_by_bus_name(bus_name)
            if bus:
                return {
                    TYPE: DATA,
                    TITLE: f'Bus Details for {bus_name}',
                    DATA: bus,
                    RETURN: '/MainMenu',
                }
            else:
                raise wz.NotFound(f'Bus with name {bus_name} not found.')
        except ValueError as e:
            raise wz.InternalServerError(f'Error: {str(e)}')


@api.route('/buses/add_bus')
class AddBus(Resource):
    """
    Adds a new bus.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.expect(bus_model)  # Create a model for the bus data
    def post(self):
        """
        Adds a new bus.
        """
        try:
            data = request.json
            bus_name = data.get('bus_name')
            borough_name = data.get('borough')
            favorite = data.get('favorite', False)

            # Call the add_bus function
            buses.add_bus(bus_name, borough_name, favorite)

            return {'message': 'Bus created successfully'}
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


@api.route('/buses/delete_bus/<bus_name>')
class DelBus(Resource):
    """
    Deletes a bus by bus name
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def delete(self, bus_name):
        """
        Deletes a bus by bus name
        """
        try:
            buses.del_bus(bus_name, True)
            return {bus_name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/form')
class Form(Resource):
    """
    This class serves the dropdown form fields.
    """
    def get(self):
        """
        Returns the dropdown form fields.
        """
        return {
            'fields': form.get_form()
        }


if __name__ == '__main__':
    app.run(debug=True)
