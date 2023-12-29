#Enroll DB data
import sqlite3
import random
import os
import hashlib


# Connect to the SQLite database
conn = sqlite3.connect('atm_database.db')
cursor = conn.cursor()

account_id = int(input("Enter Account id"))
account_name = str(input("Enter user name"))
balancep = random.randrange(100,1000000)
#balancep = int(input("Enter balance"))

# Insert account details into the 'accounts' table
def insert_account(account_number, account_holder, balance):
    cursor.execute('INSERT INTO accounts VALUES (?, ?, ?)', (account_number, account_holder, balance))
    conn.commit()

# Insert fingerprint templates into the 'fingerprints' table
def insert_fingerprint(account_number, fingerprint_data):
    cursor.execute('INSERT INTO fingerprints VALUES (?, ?)', (account_number, fingerprint_data))
    conn.commit()

# Function to securely hash and salt a password
def hash_password(pdassword, salt_length=16):
    salt = os.urandom(salt_length)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, password_hash

# Example usage
insert_account(account_id, account_name, balancep)

cursor.execute("SELECT account_holder FROM accounts WHERE account_number = ?", (account_id,))
result = cursor.fetchone()

# Check if a result was found
if result:
    user_id = result[0]
    print(f"User ID corresponding to entered ID {account_id} is: {user_id}")
    password = str(input("Create PIN (Only 4 digit): "))
    salt, password_hash = hash_password(password)
    cursor.execute("INSERT INTO security (password_hash, salt, account_number) VALUES (?, ?, ?)",
               (password_hash.hex(), salt.hex(), account_id))
else:
    print(f"No user found with the entered ID {account_id}")


#insert_fingerprint(account_id, b'sensor')

conn.commit()
cursor.close()
conn.close()