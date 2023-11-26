#!/usr/bin/python3
"""The following script starts a Flask web application
listening on 0.0.0.0, port 5000 """
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)

# Defining a route for the "/hbnb_filters" endpoint with relaxed URL rules


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """The function displays the main HBnB filters HTML page."""
    # Retrieving all State and Amenity objects from the storage
    states = storage.all("State")
    amenities = storage.all("Amenity")

    # Rendering the "10-hbnb_filters.html" template with retrieved data
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)

# Registering a function to be called when the application context ends


@app.teardown_appcontext
def teardown(exc):
    """The function removes the current SQLAlchemy session."""
    storage.close()

# Running the application if executed as the main script


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
