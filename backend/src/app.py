import time
from flask import Flask, request

from db import PostgresDatabase
from getFile import get_and_parse_data
from loadTables import load_tables




#@app.route('/api/start')
def initialize_records(database):
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
		raise e

	if results is None:
		httpStatusCode = 204
		results = ''
	else:
		httpStatusCode = 200
	return (results, httpStatusCode)










