import sqlite3 

conn = sqlite3.connect('store.db')

username = 'hello'

#Create table for cart
conn.execute("""
CREATE TABLE IF NOT EXISTS cart (
    user_id INTEGER, 
    game_id INTEGER, 
    CONSTRAINT USER_GAME UNIQUE (user_id, game_id)
) 
""")
																									#FOREIGN KEY(game_id) REFERENCES games(id), FOREIGN KEY(users_id) REFERENCES users(id))
#Add game to cart
def add_game(game_id, user_id):
    print(game_id, user_id)
    conn.execute("INSERT INTO cart (game_id, user_id) VALUES (?, ?)", (game_id, user_id))
    conn.commit()
  
#Delete game in cart
def del_game(game_id, user_id):
    conn.execute("DELETE FROM cart WHERE game_id = ? AND user_id = ?", (game_id, user_id))
    conn.commit()

def get_games(user_id):
    cur = conn.cursor()
    cur.execute("SELECT game_id FROM cart WHERE user_id = ?", (user_id,))

    rows = cur.fetchall()

    result = []

    for row in rows:
        if row:
            result.append(row[0])

    conn.commit()

    return result

