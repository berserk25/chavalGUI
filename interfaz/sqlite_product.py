import sqlite3

db_name = 'database.db'

def run_query(query, parameters = ()):
	with sqlite3.connect(db_name) as conn:
		cursor = conn.cursor()
		result = cursor.execute(query, parameters)
		conn.commit()
	return result

def get_products():
	query = 'SELECT * FROM product ORDER BY name DESC'
	return run_query(query)

def add_product(name, price):
	query = 'INSERT INTO product VALUES(NULL, ?, ?)'
	parameters = (name, price)
	run_query(query, parameters)

def delete_product(name):
	query = 'DELETE FROM product WHERE name = ?'
	run_query(query, (name,))

def edit_record(newName, name, newPrice, oldPrice):
	query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
	parameters = (newName, newPrice, name, oldPrice)
	run_query(query, parameters)