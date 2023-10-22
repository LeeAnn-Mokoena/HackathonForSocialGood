from flask import Blueprint, g, render_template, request, jsonify, flash, url_for, redirect
from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv
from passageidentity import Passage, PassageError
from bson.objectid import ObjectId

load_dotenv()

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
dashboard = Blueprint('dashboard', __name__)

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
        if (request.path.startswith('/admin') or request.path.startswith('/register')):
            g.admin_request = True
            g.user = psg.authenticateRequest(request)
            return render_template('index.html', psg_app_id=PASSAGE_APP_ID)
        else:
            g.admin_request = False
    except PassageError:
        return render_template('unauthorized.html')
    

@dashboard.route('/', methods=['GET'])
def dashboard_main():
    #fetch volunteer opportunities
    organizations_list = mongo_client.volunteer_connect.organization.find()
    existing_opportunities = []
    for org in organizations_list:
        v_opportunity_list = org.get("volunteerOpportunities")
        existing_opportunities.append(v_opportunity_list)
    all_volunteer_opportunities = process_opportunities(existing_opportunities)
    return render_template('home.html', opportunities=all_volunteer_opportunities)
    
@auth.route('/register')
def register():
    return render_template('register.html', psg_app_id=PASSAGE_APP_ID)

@auth.route('/admin/register-opportunity', methods=['POST', 'GET'])
def volunteer_opportunities():
    if(request.method == 'POST' and g.admin_requst == True):
        organization_id = request.form.get('organizationId')
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')

        existing_org_id = ObjectId(organization_id)
        existing_org = mongo_client.volunteer_opportunities.volunteering_options.find_one({"_id": existing_org_id})

        if(existing_org == None):
            flash("You cannot add a volunteer option for an organization that is not registered", category='error')

        else:
            volunteer_id = mongo_client.volunteer_opportunities.volunteering_options.insert_one(
                {
                    'organization_id': organization_id,
                    'title': title,
                    'description': description,
                    'location': location,
                    'date': date,
                    'time': time
                }
            ).inserted_id
        if(volunteer_id != None):
            flash("Submitted Successfully. Thank you for your submittion!", category='success')
            return redirect(url_for(views.home))
    else:
        render_template('unauthorized.html')
    return render_template("volunteer_opportunities.html")

#helper function section
def process_opportunities(existing_opportunities):
    results = []
    for opportunity_list in existing_opportunities:
        for json_str_dict in opportunity_list:
            json_string = json.dumps(json_str_dict)
            results.extend([json.loads(json_string)])
    #pprint.pprint(results)
    return results