from flask import Flask
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from flask import Blueprint, g, render_template, request, jsonify
import os

#load_dotenv(find_dotenv())

def create_app():
    #app instance
    app = Flask(__name__)
    app.config['SECRET_KEY']  = os.environ.get("SECRET_KEY")

    from .routes.auth import auth as user_auth, main 
    
    app.register_blueprint(user_auth)
    app.register_blueprint(main)

    print('app started::')
    return app
