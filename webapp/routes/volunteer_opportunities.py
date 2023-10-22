from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from bson.objectid import ObjectId
import os
import views
from dotenv import load_dotenv
import pprint
from pymongo import MongoClient


load_dotenv()

v_opportunities = Blueprint('opportunities', __name__)

mongo_client = MongoClient(os.getenv("MONGO_URI"))

@v_opportunities.route('/register-opportunity', methods=['POST'])
def volunteer_opportunities():
    if(request.method == 'POST'):
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
    return render_template("volunteer_opportunities.html")


@v_opportunities.route('/volunteer/opportunities', methods=['GET'])
def list_volunteer_opportunities():
    if(request.method == 'GET'):
        volunteer_collection = mongo_client.volunteering_options.find()
    for v_op in volunteer_collection:
        pprint.pprint(v_op)
    return "<h2>Successfully returned</h2>"


