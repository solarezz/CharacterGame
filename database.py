import sqlite3

connection = sqlite3.connect('C:\Python\CharacterGame\CharacterGame\database.db', check_same_thread=False)
cursor = connection.cursor()

def db_table_val(user_id: int, user_name: str, user_nameid: str):
	cursor.execute('INSERT INTO users (user_id, user_name, user_nameid) VALUES (?, ?, ?)', (user_id, user_name, user_nameid))
	connection.commit()

def db_info(user_id: int):
    cursor.execute('SELECT * FROM users WHERE user_id == ?', (user_id,))
    result = cursor.fetchone()
    return result
 
def request_partner_id(request_partner_id: int, user_id: int,):
    cursor.execute('UPDATE users SET request_partner_id = ? WHERE user_id = ?', (request_partner_id, user_id))
    connection.commit()

def pet_update(pet: str, user_id: int):
    cursor.execute('UPDATE users SET pet = ? WHERE user_id = ?', (pet, user_id))
    connection.commit()
    
def petname_update(name_pet: str, user_id: int):
    cursor.execute('UPDATE users SET name_pet = ? WHERE user_id = ?', (name_pet, user_id))
    connection.commit()
    
def db_partner(partner_id: int, partner_name: str, user_id: int, username_partner: str):
    cursor.execute('UPDATE users SET partner_id = ? WHERE user_id = ?', (partner_id, user_id))
    cursor.execute('UPDATE users SET partner_name = ? WHERE user_id = ?', (partner_name, user_id))
    cursor.execute('UPDATE users SET username_partner = ? WHERE user_id = ?', (username_partner, user_id))
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