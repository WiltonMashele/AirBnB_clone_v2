#!/usr/bin/python3
"""a script that starts a Flask web application"""


from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def hello_hbnb():
    """hello_hbnb"""
    return 'Hello HBNB!'

@app.route('/hbnb')
def hbnb():
    """hbnb"""
    return 'HBNB'

@app.route('/c/<text>')
def c_with_variable(text):
    """c_with_variable"""
    text = text.replace('_', ' ')
    return "C {}".format(text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
