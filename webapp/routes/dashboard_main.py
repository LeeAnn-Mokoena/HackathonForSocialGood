from flask import Blueprint, request, render_template, jsonify, get_flashed_messages
from bson.objectid import ObjectId
from dotenv import load_dotenv
import pprint
import json
import os
from pymongo import MongoClient

load_dotenv()

dashboard = Blueprint('dashboard', __name__)

mongo_client = MongoClient(os.getenv("MONGO_URI"))

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

def process_opportunities(existing_opportunities):
    results = []
    for opportunity_list in existing_opportunities:
        for json_str_dict in opportunity_list:
            json_string = json.dumps(json_str_dict)
            results.extend([json.loads(json_string)])
    #pprint.pprint(results)
    return results
    