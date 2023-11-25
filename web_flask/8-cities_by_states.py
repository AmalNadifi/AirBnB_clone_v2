#!/usr/bin/python3
""" The following script starts Flask to run the web app"""

from flask import Flask, render_template
from models import storage
from models.state import State

# Creating a Flask web application instance
app = Flask(__name__)

# Defining a method to be executed when the application context is being torn down


@app.teardown_appcontext
def close(self):
    """Closing the session"""

    # Closing the storage session to clean up resources
    storage.close()

# Defining a route for displaying states and cities


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displaying an HTML page with states and cities"""

    # Retrieving all State instances from storage
    states = storage.all(State)

    # Rendering an HTML page with states and cities data
    return render_template('8-cities_by_states.html', states=states)

# Running the application if this script is executed directly


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
