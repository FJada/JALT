# Progress

Detail what you have already completed in your project. What requirements were met in completing these bits?

### Development Environment & Github Actions

The development environment is up and github actions is working
We did have two weeks where we ran into build breaking issues due to MongoDB, but they were fixed!

### MongoDB

**Local:** local database connection successful <br>

**Cloud:** cloud database connection successful <br>

**Backup:** <br>
`bkup.sh`: copies our MongoDB collections from the cloud to our repo and stores them as JSON files. <br>
`restore.sh`: restores the JSON backups to our local database. <br>
`common.sh`: Holds common code for the first two above. <br>

**Databases:** <br>
`users.py`: holds username, account_id, home(address), and work(address) <br>
`routes.py`: holds route_id, starting_point, ending_point <br>
`trains.py`: holds train_stops, train_schedules, train_locations <br>
`buses.py`: holds bus_name, station_name, borough, favorite, vehicle_id <br>

These developments fulfilled our MongoDB requirements.

### API Server

**API Models:** <br>
`user_model`: username model designed to hold, fetch, and add user account names and ids in MongoDB. <br>
`route_model`: route model designed to hold, fetch, and add routes in MongoDB. <br>
`bus_model`: bus model designed to hold, fetch, and add bus names, routes, and stops in MongoDB. <br>
`get_account_id_model`: model designed to retrieve an user based on their encrypted user id. <br>
`add_home_address_model`: model designed expressly to add home addresses as a new parameters to users based on username/user id. <br>

These API models were sufficient to complete at least 12 API Endpoint requirements that utilize MongoDB.

**API Endpoints:** <br>


# Goals

Set out your goals for this semester. Please detail what the requirement is that each goals will meet, and how you expect to meet it.

**Databases** <br>
Further refine databases by narrowing them down to necessary information and connecting them together with keys in order to have them properly interact with each other.

**Enhanced API Implementation** <br>
Fetch real-time MTA subway and bus data to our databases, allowing for accurate arrival times using NYC OpenData and other APIs. We can expect to meet this goal and test it in swagger, making API endpoints to test and display the most recent subway data for each train line and bus stop.

**User Authentication and Profile Management** <br>
As `users.py` is a database that records user data, like usernames, account ids, home addresses and work addresses, creating a login system and having the ability to personalize routes and destinations will be important milestones to complete while using our user data.

**Deployment Strategy** <br>
We will need to refine and continuously test our ability to deploy our application as new API endpoints are added to it. We will also need to make sure that mongoDB can be reliably tested on pythonAnywhere with swagger rather than simply being able to use swagger and run API endpoints locally.

**React Interface** <br>
We will enhance the user experience of our app by integrating a React interface. We aim to elevate the app's responsiveness, interactivity, and overall usability.

