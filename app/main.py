from flask import Blueprint, g, render_template, request, jsonify
import os
from passageidentity import Passage, PassageError
from dotenv import load_dotenv


def configure():
    load_dotenv()

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


PASSAGE_API_KEY = os.getenv("PASSAGE_API_KEY")
PASSAGE_APP_ID = os.getenv("PASSAGE_APP_ID")

try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as error:
    print(error)
    exit()

@main.route('/')
def index():
    configure()
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

@auth.route('/dashboard', methods=['GET'])
def dashboard():
    psg_user = psg.getUser(g.user)

    identifier = ""
    if psg_user.email:
        identifier = psg_user.email
    elif psg_user.phone:
        identifier = psg_user.phone
    return render_template('dashboard.html',psg_app_id=PASSAGE_APP_ID)
