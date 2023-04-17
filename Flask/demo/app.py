import sqlite3

from flask import Flask

conn = sqlite3.connect ( 'mydb.db' )
cursor = conn.cursor ()
from flask import render_template

app = Flask ( __name__ )


@app.route ( '/' )
def index():
    return render_template ( 'index.html' )
