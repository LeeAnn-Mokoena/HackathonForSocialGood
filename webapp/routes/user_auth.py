from  werkzeug.security import generate_password_hash
from flask import Blueprint, g, render_template, request, jsonify, flash, url_for
from pymongo import MongoClient
import os
import pprint
from bson.objectid import ObjectId

user_auth = Blueprint('user_auth', __name__)
mongo_client = MongoClient(os.environ.get("MONGO_URI"))

@user_auth.route("/sign-up", methods=['GET', 'POST'])
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
    return render_template("sign_up.html")

@user_auth.route('/users', methods=['GET'])
def get():
    printer = pprint.PrettyPrinter()

    users = mongo_client.volunteer_connect.user.find()
    users_collection = []
    for user in users:
       printer.pprint(user)
       users_collection.append(user) 
    return users_collection

