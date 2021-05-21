# Create a connection cursor
cursor = mysql.connection.cursor()

# Executing SQL Statements
cursor.execute(''' CREATE TABLE table_name(users) ''')
cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
cursor.execute(''' DELETE FROM table_name WHERE condition ''')

# Saving the Actions performed on the DB
mysql.connection.commit()

# Closing the cursor
cursor.close()

@app.route('/')
def hello_world():
    return 'Hello World!'
