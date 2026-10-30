import sqlite3

connection = sqlite3.connect("weather.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM weather")

for row in cursor.fetchall():
    print(row)

connection.close()