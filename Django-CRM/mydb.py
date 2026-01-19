import mysql.connector

dataBase = mysql.connector.connect(
	host = 'MySQL@123',
	user = 'root',
	passwd = 'pass123'

	)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE django_crm")

print("All Done!")
