#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def hello_hbnb():
    """Route for '/' that displays 'Hello HBNB!'"""
    return 'Hello HBNB!'

@app.route('/hbnb', methods=['GET'], strict_slashes=False)
def hbnb():
    """Route for '/hbnb' that displays 'HBNB'"""
    return 'HBNB'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
