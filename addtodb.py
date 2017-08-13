'''This program is run separately and manually to add new entries in the
csv file that is not in the database, to the database.
'''

import csv
import sqlite3

db_connection = sqlite3.connect('events.db')
db_cursor = db_connection.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS events (
serial int NOT NULL PRIMARY KEY,
eventdate date,
name varchar,
event varchar,
priority int)'''
                  )

with open('events.csv', newline='') as csvfile:
    csvobj = csv.reader(csvfile)
    serial_nums = [x[0]
                   for x in db_cursor.execute('SELECT serial FROM events')]
    for item in csvobj:
        if int(item[0]) not in serial_nums:
            db_cursor.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?)", item)

db_connection.commit()
db_connection.close()
