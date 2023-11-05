#!/usr/bin/python3
"""a script that starts a Flask web application:"""
from flask import Flask, render_template

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
def cWithVariable(text):
    """cWithVariable"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/', defaults={'text': 'is_cool'})
@app.route('/python/<text>')
def pythonWithVariable(text):
    """pythonWithVariable"""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>')
def withNumber(n):
    """withNumber"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>')
def withNumberSendWebpage(n):
    """withNumberSendWebpage"""
    return render_template('5-number.html', n=n)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
