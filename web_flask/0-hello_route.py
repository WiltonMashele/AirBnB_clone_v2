#!/usr/bin/python3
"""A simple Flask web application"""
from flask import Flask
app = Flask(__name__)

app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000

@app.route('/', methods=['GET'], strict_slashes=False)
def hello_hbnb():
    """This function handles the root URL and returns a greeting."""
    return 'Hello, HBNB!'

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])
