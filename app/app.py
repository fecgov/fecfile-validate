"""App module for testing validation architecture"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    """Hello world home page"""

    return "Hello, World!"
