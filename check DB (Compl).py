import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('atm_database.db')  # Replace with your database file name

# Create a cursor object
cursor = conn.cursor()
print("Account Information")
# Execute an SQL query to retrieve data
cursor.execute("SELECT * FROM accounts")

# Fetch and display the data
rows = cursor.fetchall()
for row in rows:
    print(row)
    
print ("Password inforamtion")
cursor.execute("SELECT * FROM security")

# Fetch and display the data
rows = cursor.fetchall()
for row in rows:
    print(row)


# Close the cursor and the database connection
cursor.close()
conn.close()
