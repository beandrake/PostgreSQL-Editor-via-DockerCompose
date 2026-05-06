import time
from flask import Flask

from db import create_connection
from getFile import get_and_parse_data
from loadTables import load_tables


# PostgreSQL
DEFAULT_DATABASE = 'postgres'
DEFAULT_USER = 'postgres'
SUPERUSER_PASSWORD = open(r'/run/secrets/db_password').read()

# Docker
DB_PORT_OUTSIDE = '5432'
DB_PORT_INSIDE = '5432'		# ports set in docker-compose.yml
DB_HOST = 'db'				# the name of the service from docker-compose.yml


#@app.route('/api/start')
def initialize_records():
	# create connection to database
	connection = create_connection(
		DEFAULT_DATABASE,
		DEFAULT_USER,
		SUPERUSER_PASSWORD,
		DB_PORT_OUTSIDE,
		DB_HOST
	)

	# get data from web endpoint
	rivenData = get_and_parse_data()

	# connect to Postgres container
	cursor = connection.cursor()

	# load tables with data from the web endpoint
	load_tables(cursor, rivenData["timestamp"], rivenData["records"])


apiReady = False
print("Initializing records...")
initialize_records()
print("Records initialized.")
apiReady = True


app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/ready')
def get_api_ready():
	return {'ready': apiReady}
