import sqlite3
import random

create_wallet_table_query = '''
CREATE TABLE IF NOT EXISTS "wallet" (
	"username"	TEXT NOT NULL UNIQUE,
	"balance"	FLOAT NOT NULL DEFAULT 0,
	PRIMARY KEY("username")
);
'''

create_pins_table_query = '''
CREATE TABLE IF NOT EXISTS "pins" (
	"pin"	TEXT NOT NULL,
	"value"	FLOAT NOT NULL,
	PRIMARY KEY("pin")
);
'''

create_misc_table_query = '''
CREATE TABLE IF NOT EXISTS "misc" (
	"username"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("username")
);
'''

def create_table(query):
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


'''
initialize (new) user record to wallet table;
set initial balance to 0 
'''
def initialize_user_balance():
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()

    get_users_query = '''
    SELECT username from users
    '''

    c.execute(get_users_query)
    users_list = c.fetchall()
    conn.commit()

    for user in users_list:
        initialize_balance_query = f'''
        SELECT username from wallet where username='{user[0]}'
        '''
        result = c.fetchone()

        if (result == None):
            c.execute("INSERT OR IGNORE INTO wallet (username, balance) VALUES (?, ?)", (user[0], 0))        
 

    conn.commit()
    conn.close()

# get balance of user
def get_balance(username):
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()
    balance = None 
    balance_query = f'''
    SELECT balance from wallet where username='{username}'
    '''
    c.execute(balance_query)
    balance = c.fetchone()
    conn.commit()
    conn.close()
    return balance[0]


# insert user in misc
def save_misc_user(username):
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()
    c.execute("DELETE FROM misc;")
    c.execute(f"INSERT OR IGNORE INTO misc (username) VALUES ('{username}');")      
    conn.commit()
    conn.close()

# remove user from misc
def get_misc_user():
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()
    balance_query = f'''
    SELECT username from misc
    '''
    c.execute(balance_query)
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result[0]

# generate pins
def generate_pins():
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()
    pins = random.randint(20, 40)
    counter = 0
    while (counter < pins):
        values = [50, 100, 200, 500]
        pin_no = random.randint(1000, 9999)
        pin_value = values[random.randint(0, 3)]
        pin_query = f'''
        SELECT pin from pins where pin='{pin_no}'
        '''
        c.execute(pin_query)
        if (c.fetchone()):
            continue
        else:
            c.execute(f"INSERT OR IGNORE INTO pins (pin,value) VALUES ('{pin_no}',{pin_value});")    
            conn.commit()  
            counter += 1
    conn.commit()
    conn.close()

def add_credits(username, value, pin):
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()    
    
    # get current balance 
    balance = get_balance(username)

    if (not value):
        value = 0
    if (not pin):
        pin = ' '
    
    # update balance by amount value
    value_update_query = f'''
    UPDATE wallet
    SET balance = {balance + float(value)}
    WHERE username = '{username}';
    '''
    c.execute(value_update_query)
    conn.commit()

    # update balance by pin 
    # check if pin exists 
    """
    pin_query = f'''
    SELECT * from pins where pin='{pin}'
    '''
    c.execute(pin_query)
    pin_result = c.fetchone()

    # add pin value to balance 
    # consume (delete) pin
    if (pin_result):
        balance = get_balance(username)
        print(pin_result)
        pin_query = f'''
        UPDATE wallet
        SET balance = {balance + pin_result[1]}
        WHERE username='{username}';
        '''
        c.execute(pin_query)
        conn.commit()

        pin_query = f'''
        DELETE from pins WHERE pin='{pin_result[0]}';
        '''
        c.execute(pin_query)
        conn.commit()
    """
    conn.close()    

def remove_credits(username, value, pin):
    conn = sqlite3.connect('appstore.db')
    c = conn.cursor()    
    
    # get current balance 
    balance = get_balance(username)

    if (not value):
        value = 0
    if (not pin):
        pin = ' '
    
    # update balance by amount value
    value_update_query = f'''
    UPDATE wallet
    SET balance = {balance - float(value)}
    WHERE username = '{username}';
    '''
    c.execute(value_update_query)
    conn.commit()


create_table(create_wallet_table_query)
create_table(create_pins_table_query)
create_table(create_misc_table_query)
#initialize_user_balance()
#print(get_balance('admin'))
#generate_pins()