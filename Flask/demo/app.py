import json
import sqlite3

import flask
import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, request
from flask_executor import Executor
from flask_socketio import SocketIO, emit

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
from flask import render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
