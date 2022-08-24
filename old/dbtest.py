import sqlite3

conn = sqlite3.connect(r'D:/Project/orders.db')


def new_func(conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
   orderid INT PRIMARY KEY,
   date TEXT,
   userid TEXT,
   total TEXT);
""")
    conn.commit()


new_func(conn)
