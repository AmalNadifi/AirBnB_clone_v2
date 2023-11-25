#!/usr/bin/python3
"""The following script starts a Flask web application
listening on 0.0.0.0, port 5000 """

from flask import Flask, render_template
from models import storage
from models.state import State

# Creating a Flask web application instance
app = Flask(__name__)

# Defining a method to be executed,
# when the application context is being torn down


@app.teardown_appcontext
def close(self):
    """Closing the session"""

    # Closing the storage session to clean up resources
    storage.close()

# Defining a route for displaying states


@app.route('/states', strict_slashes=False)
def state():
    """Displaying an HTML page with states"""

    # Retrieving all State instances from storage
    states = storage.all(State)

    # Rendering an HTML page with states data
    return render_template('9-states.html', states=states, mode='all')

# Defining a route for displaying cities of a specific state


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Displaying an HTML page with cities of the specified state"""

    # Iterating through all State instances to find the specified state
    for state in storage.all(State).values():
        if state.id == id:

            # Rendering an HTML page with cities of the specified state
            return render_template('9-states.html', states=state, mode='id')

    # Rendering an HTML page indicating that the specified state was not found
    return render_template('9-states.html', states=state, mode='none')

# Running the application if this script is executed directly


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
