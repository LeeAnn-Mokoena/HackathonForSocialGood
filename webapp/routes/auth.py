from flask import Blueprint, g, render_template, request, jsonify, flash, url_for, redirect
from pymongo import MongoClient
import os
import json
import pprint
from dotenv import load_dotenv
from passageidentity import Passage, PassageError
from bson.objectid import ObjectId
from datetime import datetime

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

@dashboard.route('user/sign-up', methods=['POST']) 
def user_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        name = request.form.get('name')
        biography = request.form.get('biography')
        volunteer_interest = request.form.get('volunteerInterest')

    existing_org = get_org_from_opportunity_title(volunteer_interest)
    if existing_org == None:
        flash("That title does not have an organization associated with it. Please try again")
    else:
        v_opportunity = query_org_opportunity(existing_org.__id, volunteer_interest)
        v_opportunity_submit = {'title': v_opportunity.title,
               'description': v_opportunity.description,
               'dateOfRequest': datetime.now().date(),
               'timeOfRequest': datetime.now().time()
               }
        inserted_id = mongo_client.volunteer_connect.user.insert_one({
            'name': name,
            'userName': user_name,
            'email': email,
            'biography': biography,
            'preferredContactMethod': 'email',
            'volunteerInterests': v_opportunity_submit,
            'status': 'Pending'
                  }).inserted_id
        if inserted_id != None:
            print("inserted id", inserted_id)
            flash("Successfully Submitted volunteer interest. Your submission is now being reviewed")
    return render_template('sign_up.html')  



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
    return results

def get_org_from_opportunity_title(opportunity_title):
    return mongo_client.volunteer_connect.organization.find({"volunteerOpportunities.title":opportunity_title})

def query_org_opportunity(existing_org_id, volunteer_interest):
    title_to_match = volunteer_interest
    document_result = mongo_client.volunteer_connect.organization.aggregate([
        {
            "$match": {"_id":existing_org_id}
        },
        {
        "$project": {
            "matchedData": {
                "$filter": {
                    "input": "$nestedData",
                    "as": "item",
                    "cond": {"$eq": ["$$item.title", title_to_match]}
                }}
            }
        }
    ])
    matched_result = list(document_result)[0]["matchedData"]
    print("matched data found=============================")
    pprint(matched_result)
    return matched_result


