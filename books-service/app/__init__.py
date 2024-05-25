from flask import Flask
from flask_pymongo import PyMongo
from .routes import api_blueprint
from .rating import ratings_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/books')

    mongo = PyMongo(app)
    app.mongo = mongo

    app.register_blueprint(api_blueprint)
    app.register_blueprint(ratings_blueprint)

    return app



