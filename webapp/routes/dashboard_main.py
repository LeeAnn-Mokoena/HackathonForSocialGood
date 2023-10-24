from flask import Blueprint, request, render_template,flash
from bson.objectid import ObjectId
from dotenv import load_dotenv
import json
import os
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

dashboard = Blueprint('dashboard', __name__)

mongo_client = MongoClient(os.getenv("MONGO_URI"))

@dashboard.route('/', methods=['GET'])
def dashboard_main():
    organizations_list = mongo_client.volunteer_connect.organization.find()
    existing_opportunities = []
    for org in organizations_list:
        v_opportunity_list = org.get("volunteerOpportunities")
        existing_opportunities.append(v_opportunity_list)
    all_volunteer_opportunities = process_opportunities(existing_opportunities)
    return render_template('home.html', opportunities=all_volunteer_opportunities)

@dashboard.route('/user/sign-up', methods=['POST', 'GET']) 
def user_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        name = request.form.get('name')
        biography = request.form.get('biography')
        volunteer_interest = request.form.get('volunteerInterest')

        existing_org = get_org_from_opportunity_title(volunteer_interest)
        org_id = extract_document_id(existing_org)
        matched_opportunity = extract_nested_document(org_id,volunteer_interest)
        if existing_org == None:
            flash("That title does not have an organization associated with it. Please try again")
        else:
            v_opportunity_submit = {'title': matched_opportunity['title'],
                'description': matched_opportunity['description'],
                'dateOfRequest': datetime.now().date().strftime('%Y-%m-%d'),
                'timeOfRequest': datetime.now().time().strftime('%H:%M:%S')
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
                flash("Successfully Submitted volunteer interest. Your submission is now being reviewed")
    return render_template('sign_up.html')  

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

def extract_document_id(existing_org):
      for document in existing_org:
          org_id = document['_id']
      return org_id

def extract_nested_document(org_id, title_to_match):
    org_query = {"_id": ObjectId(org_id)}
    org = mongo_client.volunteer_connect.organization.find_one(org_query)
    nested_documents = org.get("volunteerOpportunities",[])
    filtered_nested_doc = next((v_opportunity for v_opportunity in nested_documents if v_opportunity.get("title") == title_to_match), None)
    return filtered_nested_doc