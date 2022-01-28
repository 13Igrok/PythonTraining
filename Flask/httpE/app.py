import json
import os
import re
import ssl
from dataclasses import fields
from datetime import datetime
from sqlite3 import apilevel
from urllib.request import urlopen

from flask import (Flask, Response, jsonify, make_response, render_template,
                   request)

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index(username):
    return "Hello, %s!" % username


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


@app.route('/login')
def index():
    return render_template('login.html')


@app.route('/FlaskTutorial',  methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        return render_template('success.html', email=email)
    else:
        pass


@app.route('/blogs')
def blog():
    return render_template('blog.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
