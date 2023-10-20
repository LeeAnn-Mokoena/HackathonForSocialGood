from webapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""from flask import Blueprint, g, render_template, request, jsonify
import os
import pprint
from passageidentity import Passage, PassageError
from dotenv import load_dotenv, find_dotenv
#from .extensions import mongo
from  werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

load_dotenv(find_dotenv())

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)"""


#PASSAGE_API_KEY = os.getenv("PASSAGE_API_KEY")
#PASSAGE_APP_ID = os.getenv("PASSAGE_APP_ID")
#mongo_connection = os.environ.get("CONNECTION_CLOUD")

#client = MongoClient(mongo_connection)

#retrieve the database and contents (i.e collection)
#db = client["volunteer_connect"]
#collection  = db["user"]
"""user_details = {
    "userName": "mTroy", "email": "troy@gmail.com","password":"test20", "name":"Tony",
    "location": "Plainfield,NJ", "biography": "passionate with a heart to serve",
    "contactInformation": "8798765678"
}"""
#details = collection.find_one({"userName": "mTroy"})
#print (details)
#print(list(collection.find()))
#collection.delete_one({"email": "troy@gmail.com"} )
"""print(db)
print(collection)"""

"""try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as error:
    print(error)
    exit()"""

"""@main.route('/')
def index():
    
    user_collection = mongo.local.user
    user_collection.insert({'name': 'Anthony'})
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

@auth.route('/dashboard', methods=['GET'])
def dashboard():
    psg_user = psg.getUser(g.user)

    identifier = ""
    if psg_user.email:
        identifier = psg_user.email
    elif psg_user.phone:
        identifier = psg_user.phone
    return render_template('dashboard.html',psg_app_id=PASSAGE_APP_ID)"""
