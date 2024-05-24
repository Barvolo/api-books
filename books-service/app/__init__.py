from flask import Flask
from .routes import api_blueprint
from .rating import ratings_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)

    app.register_blueprint(ratings_blueprint)
    return app
