import sqlite3

connection = sqlite3.connect('C:\Python\CharacterGame\CharacterGame\database.db', check_same_thread=False)
cursor = connection.cursor()

def db_table_val(user_id: int, user_name: str):
	cursor.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
	connection.commit()
 
def db_info_pet(user_id: int):
    cursor.execute('SELECT pet FROM users WHERE user_id == ?', (user_id,))
    result = cursor.fetchone()
    return result
    
def db_info_username(user_id: int):
	cursor.execute('SELECT user_name FROM users WHERE user_id == ?', (user_id,))
	result = cursor.fetchone()
	return result

def update_info(user_id: int, pet: str, name_pet: str):
    cursor.execute('UPDATE users WHERE user_id = ? SET pet = ? AND name_pet = ?', user_id, pet, name_pet)