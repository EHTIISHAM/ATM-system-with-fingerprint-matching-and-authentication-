import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('atm_database.db')
cursor = conn.cursor()

# Create a table to store account details
cursor.execute('''CREATE TABLE accounts (
                    account_number TEXT PRIMARY KEY,
                    account_holder TEXT,
                    balance REAL
                )''')


#create password-hash table
cursor.execute('''CREATE TABLE security(
                    password_hash TEXT,
                    salt TEXT NOT NULL,
                    account_number TEXT,
                    FOREIGN KEY (account_number) REFERENCES accounts (account_number)
                )''')

# Close the database connection when done
conn.close()
