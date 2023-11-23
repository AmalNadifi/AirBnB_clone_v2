#!/usr/bin/python3
""" 
The following script starts a Flask web application:
The web application must be listening on 0.0.0.0, port 5000
"""

from flask import Flask, render_template
from markupsafe import escape

# Creating a Flask application instance
app = Flask("__name__")

# Defining a route for the ("/") and disable strict slashes for flexibility
@app.route('/', strict_slashes=False)
def hello():
    """Return a given string"""
    # This function will be executed when the root URL is accessed
    return ("Hello HBNB!")

# Defining a route for "/hbnb" and disabling strict slashes
@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns a given string"""
    # This function will be executed when the "/hbnb" URL is accessed
    return ("HBNB")

@app.route('/c/<text>', strict_slashes=False)
def cText(text):
    # Using the markupsafe.escape function to prevent XSS attacks
    return "C {}".format(escape(text.replace("_", " ")))

# Defining a route for "/python/" and "/python/<text>" with a default value for text
@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    # Using the markupsafe.escape function to prevent XSS attacks
    return "Python {}".format(escape(text.replace("_", " ")))

# Defining a route for "/number/<int:n>" and disable strict slashes
@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    # Function for "/number/<int:n>", displays "{} is a number"
    return '{} is a number'.format(n)

# Defining a route for "/number_template/<int:n>" and disabling strict slashes
@app.route('/number_template/<int:n>', strict_slashes=False)
def rendering_number_template(n):
    # Rendering the template and passing the number as a variable
    if isinstance(n, int):
        return render_template("5-number.html", n=n)

# Running the Flask application if this script is executed directly
if __name__ == "__main__":
    # Starting the Flask development server to listen on 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000)
