from flask import Flask
import pymongo
from pymongo import mongo_client

client = mongo_client("connection string here")
db = client["name of client"]
document = db["specific document"]

def create_app():
    app = Flask(__name__)

    from .main import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
