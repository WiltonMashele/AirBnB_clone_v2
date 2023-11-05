#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /hbnb: HBnB home page.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)

# Define the route for the HBnB home page
@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Displays the main HBnB filters HTML page.
    """
    # Retrieve data from the storage
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template(
            "100-hbnb.html", states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
