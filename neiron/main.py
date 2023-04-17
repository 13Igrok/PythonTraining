import sqlite3

conn = sqlite3.connect ( 'mydatabase.db' )
c = conn.cursor ()

conn.commit ()
conn.close ()
