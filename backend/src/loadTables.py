


def load_tables(cursor, timestamp, fullRecords):
	_load_temp_table(cursor, timestamp, fullRecords)
	_load_weapon_types_table(cursor)
	_load_weapons_table(cursor)
	_load_trades_table(cursor)
	

def queryDisplay(cursor, query):
	print("Executing the following query:")
	print(query)
	cursor.execute(query)
	
	print("Results of query:")
	result = cursor.fetchone()
	while result is not None:
		print(result)
		result = cursor.fetchone()


def _load_temp_table(cursor, timestamp, fullRecords):
	# Make temp table for all records from datafile
	query="""
		CREATE TEMP TABLE temp_data (
			id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
			itemType VARCHAR(255),
			weapon VARCHAR(255),
			rerolled BOOL,
			avg FLOAT,
			stddev FLOAT,
			min INT,
			max INT,
			pop INT,
			median INT,
			uploaded TIMESTAMP
		);
	"""
	cursor.execute(query)

	# populate with (mostly) unfiltered data
	query="""
		INSERT INTO temp_data (
			itemType, weapon, rerolled, avg, 
			stddev, min, max, pop, median, uploaded
		)
		VALUES (
			--split_part to get first word; example: "Shotgun Riven Mod"
			split_part(%(itemType)s, ' ', 1), --isolate first term
			%(compatibility)s, %(rerolled)s, %(avg)s,
			%(stddev)s, %(min)s, %(max)s, %(pop)s, %(median)s, %(timestamp)s
			);
	"""
	for record in fullRecords:
		record["timestamp"] = timestamp
		cursor.execute(query, record)

	# Optional verification output
	query="SELECT * FROM temp_data;"
	queryDisplay(cursor, query)


def _load_weapon_types_table(cursor):
	# Make weapon_types table
	query="""
		CREATE TABLE weapon_types (
			id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
			name VARCHAR(255) UNIQUE
		);
	"""
	cursor.execute(query)

	# populate from temp_data
	query="""
		INSERT INTO weapon_types (name)
		SELECT DISTINCT itemType
		FROM temp_data;
	"""
	cursor.execute(query)

	# Optional verification output
	query="SELECT * FROM weapon_types;"
	queryDisplay(cursor, query)


def _load_weapons_table(cursor):
	# Make weapons table
	query="""
		CREATE TABLE weapons (
			id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
			name VARCHAR(255) UNIQUE,
			type_id INT REFERENCES weapon_types (id)
		);
	"""
	cursor.execute(query)

	# populate from temp_data
	query="""
		INSERT INTO weapons (name, type_id)
		SELECT DISTINCT weapon, weapon_types.id
		FROM temp_data
		LEFT JOIN weapon_types ON
			weapon_types.name = temp_data.itemType
		WHERE weapon IS NOT NULL;
	"""
	cursor.execute(query)

	# Optional verification output
	query="SELECT * FROM weapons ORDER BY name;"
	queryDisplay(cursor, query)


def _load_trades_table(cursor):
	# Make trades table
	query="""
		CREATE TABLE trades (
			id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
			weapon_id INT REFERENCES weapons (id),
			rerolled BOOL,
			avg FLOAT,
			stddev FLOAT,
			min INT,
			max INT,
			median INT,
			uploaded TIMESTAMP
		);
	"""
	cursor.execute(query)

	# populate from temp_data
	query="""
		INSERT INTO trades
			(weapon_id, rerolled, avg, stddev, min, max, median, uploaded)
		SELECT DISTINCT
			weapons.id, rerolled, avg, stddev, min, max, median, uploaded
		FROM temp_data
		LEFT JOIN weapons ON
			weapons.name = temp_data.weapon
		WHERE weapon IS NOT NULL;
	"""
	cursor.execute(query)

	# Optional verification output
	query="""
		SELECT
			weapons.name, rerolled, weapon_types.name,
			avg, stddev, min, max, median, uploaded
		FROM trades
		LEFT JOIN weapons ON
			weapons.id = trades.weapon_id
		LEFT JOIN weapon_types ON
			weapon_types.id = weapons.type_id
		ORDER BY weapons.name, rerolled;
	"""
	queryDisplay(cursor, query)

