import psycopg2 as pg

# PostgreSQL database info
DEFAULT_DATABASE = 'postgres'
DEFAULT_USER = 'postgres'
SUPERUSER_PASSWORD = open(r'/run/secrets/db_password').read()

# PostgresSQL container info
DB_HOST = 'db'			# the name of the service from docker-compose.yml
DB_PORT = '5432'		# ports set in docker-compose.yml

class PostgresDatabase:
	def __init__(self):
		self.connection = None
		kwargs = {
			'database': DEFAULT_DATABASE,
			'user': DEFAULT_USER,
			'password': SUPERUSER_PASSWORD,
			'port': DB_PORT,
			'host': DB_HOST		# not needed if in same container/server
		}
		try:
			print("Connecting to PostgreSQL DB...")
			self.connection = pg.connect(**kwargs)
			print("Successfully connected to PostgreSQL DB.")
		except pg.OperationalError as e:
			print("Error when attempting to connect to PostgreSQL DB:\n" + str(e))
			raise e	

	def runQuery(self, query, values=[]):
		"""
		Run the query and return the results into a dictionary containing
		two items: headers and records.
		"""
		cursor = self.getCursor()
		cursor.execute(query, values)
		self.connection.commit()
		
		# If there are no results, we're done.
		if cursor.description == None:
			return None
		
		# Get the headers and the records and return them as a dictionary
		headerList = [desc[0] for desc in cursor.description]
		recordList = []
		for record in cursor:
			recordList.append(record)
		return {
			"headers": headerList,
			"records": recordList
		}

	def displayQueryOutput(self, query, values=[]):
		print("Executing the following query:")
		print(query)
		cursor = self.getCursor()
		cursor.execute(query)	
		print("Results of query:")
		headerList = [desc[0] for desc in cursor.description]
		print(headerList)
		result = cursor.fetchone()
		while result is not None:
			print(result)
			result = cursor.fetchone()
		self.connection.commit()
	
	def rollback(self):
		self.connection.rollback()

	def getCursor(self):
		return self.connection.cursor()
	








