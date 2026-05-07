import time
from flask import Flask, request

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


class PostgresDatabase:
	def __init__(self):
		self.connection = create_connection(
			DEFAULT_DATABASE,
			DEFAULT_USER,
			SUPERUSER_PASSWORD,
			DB_PORT_OUTSIDE,
			DB_HOST
		)
		self.cursor = self.connection.cursor();

	def runQuery(self, query, values=[]):
		"""
		Run the query and return the results into a dictionary containing
		two items: headers and records.
		"""
		self.cursor.execute(query, values)
		headerList = [desc[0] for desc in self.cursor.description]
		recordList = []
		for record in self.cursor:
			recordList.append(record)
		
		self.connection.commit()
		return {
			"headers": headerList,
			"records": recordList
		}
	
	def rollback(self):
		self.connection.rollback()

	def getCursor(self):
		return self.cursor


#@app.route('/api/start')
def initialize_records(database):
	# create connection to database
	#connection = create_connection(
	#	DEFAULT_DATABASE,
	#	DEFAULT_USER,
	#	SUPERUSER_PASSWORD,
	#	DB_PORT_OUTSIDE,
	#	DB_HOST
	#)

	# get data from web endpoint
	rivenData = get_and_parse_data()

	# connect to Postgres container
	cursor = database.getCursor()

	# load tables with data from the web endpoint
	load_tables(cursor, rivenData["timestamp"], rivenData["records"])


apiReady = False
database = PostgresDatabase()
print("Initializing records...")
initialize_records(database)
print("Records initialized.")
apiReady = True


app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/ready')
def get_api_ready():
	return {'ready': apiReady}


# Runs any query the user submits.
@app.route('/api/query', methods=['GET', 'POST'] )
def get_api_query():
	dictionary = request.args
	print(dictionary)
	query = dictionary['query']
	print(query)
	
	#database = PostgresDatabase()
	try:
		results = database.runQuery(query)
		print(results)
	except Exception as e:
		print(f'Error: {e}')
		database.rollback()	

	return results










