#!/usr/bin/python3
"""The follwoing module starts a FLASK WEB APPLICATION"""

from flask import Flask
# Creating a Flask application instance
app = Flask(__name__)

# Defining a route for ("/") & disable strict slashes for flexibility
@app.route("/", strict_slashes=False)
def index():
    """This function will be executed when the root URL is accessed """
    return "Hello HBNB!"

# Running the Flask application if this script is executed directly
if __name__ == "__main__":
    # Starting the Flask development server to listen on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000)
