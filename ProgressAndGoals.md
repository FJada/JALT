# Progress

Detail what you have already completed in your project. What requirements were met in completing these bits?

### Development Environment & Github Actions

### Fancier Testing

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

# Goals

Set out your goals for this semester. Please detail what the requirement is that each goals will meet, and how you expect to meet it.

**Databases:** <br>
Further refine databases by narrowing them down to necessary information and connecting them together with keys in order to have them properly interact with each other.
