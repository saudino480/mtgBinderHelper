import sqlite3
import click
import json
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def data_helper(value, cols, table, debug = 0):
	'''
	Returns the values for each of the columns supplied.
	Due to name limitations between the JSON and the SQLite DB
	we have to use a function to parse the values instead of a
	regular dictonary; the scryfallId, as well as some other columns,
	are nested dictonaries, that need to be keyed into a specific way.

	Takes:
	value: List A list of dictonaries representing the rows.
	cols: List A list of strings representing the columns of the table 
		  in our DB.
	table: STR A string representing the name of one of the tables in the
		   DB.

	Returns:
	data: a tuple containing the desired values, to be used in a SQLite query.
	'''
	if debug > 1:
		print(f"Cols: {cols}")

	exception_flag = False
	
	table_dict = {'cardInfo' : {
		'setId' : 'setCode',
		'setNumber' : 'number',
		'scryfallId' : ('identifiers', 'scryfallId'),
		'oracle' : 'text',
		},
		'collection' : {'temp' : 'value'},
		'priceHistory' : {'temp' : 'value'},
		'setInfo' : {'setCode' : 'code'},
		'user' : {'temp' : 'value'}
	}

	conversion_dict = table_dict.get(table, None)

	if not conversion_dict:
		print(f"{table} is not a valid table. No conversion performed.")
		return tuple(value.get(col, None) for col in cols)

	if table == 'cardInfo':
		exception_flag = value['name'].find(r"//") != -1
		exception_flag = value['type'].lower().find('land') != -1
		exception_flag = not value.get('text', False)
		value['hasFoil'] = not value.get('hasFoil', True)
		value['hasNonFoil'] = not value.get('hasNonFoil', True)
	elif table == 'setInfo':
		value['block'] = value.get('block', 'NA')


	data = []
	fixed_cols = [conversion_dict.get(col, col) for col in cols]
	if debug > 1:
		print(f"fixed_cols: {fixed_cols}")
	for col in fixed_cols:
		val = value.get(col, None)
		if not val:
			try:
				val = value[col[0]][col[1]]
			except:
				# exceptions still need to be fixed
				# more investigations forthcoming
				# if not exception_flag and "Foil" not in col:
				# 	print(f"Column {col} not found. None was replaced as the value.")
				# 	print(f"Offending card: {value['name']}")
				val = None
			data.append(val)
		else:
			if isinstance(val, list):
				val = ", ".join(val)
			data.append(val)


	return tuple(data)




def init_db(debug = 1):
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

	# needs to be some kind of "load in" function
	loadedJSON = json.load(open("data/AllPrintings.json"))
	date = loadedJSON['meta']['date']
	card_ref = loadedJSON['data']
	del loadedJSON

	if debug > 0:
		print("*"*50, "Initializing Database. This will take a few minutes.", sep="\n")
	# load set data

	# here we are getting the column names to be more flexible
	# this way we can expand what the DB does at some point and
	# be able to reinitialize it on a new machine
	# the indexing [1:] is to remove the 'id' column.
	cardInfo_cols = db.execute("SELECT * FROM cardInfo").description
	cardInfo_cols = [col[0] for col in cardInfo_cols[1:]]
	setInfo_cols = db.execute("SELECT * FROM setInfo").description
	setInfo_cols = [col[0] for col in setInfo_cols[1:]]

	if debug > 1:
		print(f"cardInfo_cols: {cardInfo_cols}")

	for (key, value) in card_ref.items():

		query = f"INSERT INTO setInfo {tuple(setInfo_cols)}" + f" VALUES ({', '.join(['?']*len(setInfo_cols))})"
		data = data_helper(value, setInfo_cols, 'setInfo', debug)

		if debug > 0:
			print(f"Commiting {value['name']} to the setInfo table.")
			if debug > 2:
				print(f"Data: {data}")
				print("-"*50)
				print(f"Query: {query}")

		db.execute(query, data)
			# (key, 
			#  value['name'], value.get('block', 'NA'), value['releaseDate'], 
			#  value['baseSetSize'], value['totalSetSize'], value['type'],)
		db.commit()
		#print(f"Commiting {value['name']} to the setInfo table.")
		
		# there has got to be a better way
		# should probably write a function to handle the names


		for card in value['cards']:
			query = f"INSERT INTO cardInfo {tuple(cardInfo_cols)}" + f" VALUES ({', '.join(['?']*len(cardInfo_cols))})"
			data = data_helper(card, cardInfo_cols, 'cardInfo', debug)
			if debug > 1:
				print(f"Commiting {card['name']} to the cardInfo table.")
				if debug > 2:
					print(f"Data: {data}", f"Query: {query}", sep = "\n" + "-"*50 + "\n")
			db.execute(query, data)

				# 'INSERT INTO cardInfo (' + ", ".join(card_cols) + ')' +
				# ' VALUES (' + ", ".join(['?']*len(card_cols)) + 
				# ")", (key,) + tuple(value.get(col, "NA") for col in card_cols)
			db.commit()
		if debug > 0:
			print(f"Finished with all cards from {value['name']} to the cardInfo table.")



@click.command('init-db')
@with_appcontext
def init_db_command():
	'''Clear existing data and create new tables.'''
	init_db()
	click.echo('Initialized DBs.')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)