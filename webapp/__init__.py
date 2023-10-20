from flask import Flask
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from flask import Blueprint, g, render_template, request, jsonify
import os

#load_dotenv(find_dotenv())

def create_app():
    #app instance
    app = Flask(__name__)
    #app.config['PASSAGE_API_KEY'] = os.getenv("PASSAGE_API_KEY")
    #app.config['PASSAGE_APP_ID'] = os.getenv("PASSAGE_APP_ID")
    app.config['SECRET_KEY']  = os.environ.get("SECRET_KEY")

    from .routes.user_auth import user_auth
    
    app.register_blueprint(user_auth)

    print('app started::')
    return app
