import sqlite3

connection = sqlite3.connect('C:\Python\CharacterGame\CharacterGame\database.db', check_same_thread=False)
cursor = connection.cursor()

def db_table_val(user_id: int, user_name: str):
	cursor.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
	connection.commit()

