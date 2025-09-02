"""A simple Flask application that returns 'Hello, World!'."""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def greet(name):
    """Return a greeting for the given name."""
    return f"Hello {name}"
