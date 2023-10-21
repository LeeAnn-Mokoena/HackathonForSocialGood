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
mongo_client = MongoClient(os.getenv("MONGO_URI"))

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

@auth.route('/{id}/dashboard', methods=['GET'])
def dashboard():
    psg_user = psg.getUser(g.user)
    print("psg user", psg_user)

    identifier = ""
    if psg_user.email:
        identifier = psg_user.emaill
    elif psg_user.phone:
        identifier = psg_user.phone
    return render_template('dashboard.html', psg_app_id=PASSAGE_APP_ID)

"""@auth.route('/user', methods=['POST'])
def create_user():
    print("creating user")
    print(request.get_json()["name"])
    print("whats value of g:", g)"""




"""@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name  = request.form.get('lastName')
        biography = request.form.get('biography')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')

        if len(email) < 4:
            flash("email cannot be greater than 4 characters long")
        elif len(first_name) < 2:
            flash("last name must be greater than 2 characters", category='error')
        elif pwd1 != pwd2:
            flash("passwords do not match", category='error')
        elif len(pwd1) < 7:
            flash("password must be at least 7 characters", category='error')
        else:
            user_entry = {
                "email": email,
                "userName": user_name,
                "firstName": first_name,
                "lastName": last_name,
                "biography": biography,
                "password": generate_password_hash(pwd1, method='pbkdf2:sha256:600000')
            }
            user_id = mongo_client.volunteer_connect.user.insert_one(user_entry).inserted_id
            print("inserted id", user_id)
    return render_template("sign_up.html")"""

"""@auth.route('/users', methods=['GET'])
def get():
    printer = pprint.PrettyPrinter()

    users = mongo_client.volunteer_connect.user.find()
    users_collection = []
    for user in users:
       printer.pprint(user)
       users_collection.append(user) 
    return users_collection"""