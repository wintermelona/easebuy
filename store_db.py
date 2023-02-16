import sqlite3 
import datetime

conn = sqlite3.connect('store.db')

username = 'hello'

#Create table for cart
conn.execute("""
CREATE TABLE IF NOT EXISTS cart (
    username TEXT, 
    game_id INTEGER, 
    CONSTRAINT USER_GAME UNIQUE (username, game_id)
) 
""")
             
conn.execute("""
CREATE TABLE IF NOT EXISTS user_library (
    username TEXT, 
    game_id INTEGER, 
    price FLOAT,
    purchase_time TIMESTAMP,
    CONSTRAINT USER_GAME UNIQUE (username, game_id)
) 
""")
																									#FOREIGN KEY(game_id) REFERENCES games(id), FOREIGN KEY(users_id) REFERENCES users(id))
#Add game to cart
def add_game(game_id, username):
    print(game_id, username)
    conn.execute("INSERT INTO cart (game_id, username) VALUES (?, ?)", (game_id, username))
    conn.commit()
  
#Delete game in cart
def del_game(game_id, username):
    conn.execute("DELETE FROM cart WHERE game_id = ? AND username = ?", (game_id, username))
    conn.commit()

def get_games(username):
    cur = conn.cursor()
    cur.execute("SELECT game_id FROM cart WHERE username = ?", (username,))

    rows = cur.fetchall()

    result = []

    for row in rows:
        if row:
            result.append(row[0])

    conn.commit()

    return result

def add_library_game(game_id, username, price):
    conn.execute("INSERT INTO user_library (game_id, username, price, purchase_time) VALUES (?, ?, ?, ?)", (game_id, username, price, datetime.datetime.now()))
    conn.commit()
  
#Delete game in cart
def del_library_game(game_id, username):
    conn.execute("DELETE FROM user_library WHERE game_id = ? AND username = ?", (game_id, username))
    conn.commit()

def get_library_games(username):
    cur = conn.cursor()
    cur.execute("SELECT game_id FROM user_library WHERE username = ?", (username,))

    rows = cur.fetchall()

    result = []

    for row in rows:
        if row:
            result.append(row[0])

    conn.commit()

    return result

def get_library_games_all_data(username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_library WHERE username = ?", (username,))

    rows = cur.fetchall()

    result = []

    for row in rows:
        if row:
            result.append(row)

    conn.commit()

    return result