#from  werkzeug.security import generate_password_hash
from flask import Blueprint, g, render_template, request, jsonify, flash, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from passageidentity import Passage, PassageError
import jwt
#import pprint
#from bson.objectid import ObjectId

load_dotenv()

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)


API_URL = os.getenv("API_URL")

PASSAGE_API_KEY = os.getenv("PASSAGE_API_KEY")
PASSAGE_APP_ID = os.getenv("PASSAGE_APP_ID")


try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as e:
    print(e)
    exit()


@auth.before_request
def before_request():
    try:
        g.user = psg.authenticateRequest(request)
        print("g user", g.user)
    except PassageError as e:
        print(f"PassageError: {str(e)}")
        cookies = request.cookies
        print("request headers", cookies)
        return render_template('unauthorized.html')
    
@auth.route('/register')
def register():
    return render_template('register.html', psg_app_id=PASSAGE_APP_ID)

@main.route('/')
def index():
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

@auth.route('/dashboard', methods=['GET'])
def dashboard():
    psg_user = psg.getUser(g.user)
    print("psg user", psg_user)

    identifier = ""
    if psg_user.email:
        identifier = psg_user.emaill
    elif psg_user.phone:
        identifier = psg_user.phone
    return render_template('dashboard.html', psg_app_id=PASSAGE_APP_ID)