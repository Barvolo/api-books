from flask import Flask
from flask_pymongo import PyMongo
from .routes import loans_bp
import os

def create_app():
    app = Flask(__name__)
    # Get MONGO_URI from environment variable or use default for local development
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/loans')
    app.config["MONGO_URI"] = mongo_uri
    
    mongo = PyMongo(app)
    
    app.register_blueprint(loans_bp)
    
    # Attach mongo to the app for easy access in routes
    app.mongo = mongo
    
    return app