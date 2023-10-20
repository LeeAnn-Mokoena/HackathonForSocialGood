from  werkzeug.security import generate_password_hash
from flask import Blueprint, g, render_template, request, jsonify, flash, url_for
from pymongo import MongoClient
import os

user_auth = Blueprint('user_auth', __name__)
mongo_client = MongoClient(os.environ.get("MONGO_URI"))

@user_auth.route("/login", methods=['GET', 'POST'])
def login():
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

