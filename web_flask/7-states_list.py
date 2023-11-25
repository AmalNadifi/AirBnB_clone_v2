#!/usr/bin/python3
""" The following script starts a Flask web application
listening on 0.0.0.0, port 5000.
"""

from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_state():
    """
    This function returns an HTML page that displays all states
    """
    # Retrieving all State instances from the storage
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    # Rendering the HTML template, passing the list of states to the template
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(excep):
    """
    The function calls the Storage.close method,
    when the app context is torn down
    """
    storage.close()


if __name__ == "__main__":
    # Running the Flask application on 0.0.0.0
    # (all available network interfaces) and port 5000
    app.run(host="0.0.0.0", port=5000)
