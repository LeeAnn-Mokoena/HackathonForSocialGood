from flask import Blueprint, g, render_template, request, jsonify, flash, url_for, redirect
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from passageidentity import Passage, PassageError
from bson.objectid import ObjectId

load_dotenv()
auth = Blueprint('auth', __name__)

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

@auth.route('/register')
def register():
    return render_template('register.html', psg_app_id=PASSAGE_APP_ID)

@auth.route('/admin/register-org', methods=['POST', 'GET'])
def register_organization():
    if request.method == 'POST' and g.admin_request == True:
        organization_name = request.form.get('org-name')
        existing_org = get_org_from_name(organization_name)
        if existing_org != None:
            flash("Organization already exists. Update the organization instead")
            redirect(url_for('organizations.create_organization'))
        else:
            org_bio = request.form.get('description')
            location = request.form.get('location')
            contact_info = request.form.get('contactInformation')
            volunteer_opp_title = request.form.get('opportunityTitle')
            volunteer_opp_description = request.form.get('opportunityDescr')
            date = request.form.get('date')
            start_time = request.form.get('startTime')
            end_time = request.form.get('endTime')
            location_type = request.form.get('locationType')

            volunteer_opportunity = [{
                'title': volunteer_opp_title,
                'description': volunteer_opp_description,
                'date': date,
                'startTime': start_time,
                'end_Time': end_time,
                'locationType': location_type
            }]

            existing_org = mongo_client.volunteer_opportunities.volunteering_options.find_one({"name": organization_name})
            if existing_org != None:
                flash("Organization with the same name already exists. Organization name needs to be different to avoid confusion")
            else:
                inserted_id = mongo_client.volunteer_connect.organization.insert_one({
                    'name': organization_name,
                    'description': org_bio,
                    'location': location,
                    'contactInformation': contact_info,
                    'volunteerOpportunities': volunteer_opportunity
                })
                print("inserted id/////////", inserted_id)

            
                return redirect(url_for('views.home'))
    elif g.admin == False:
        render_template('unauthorized.html')
    return render_template("organization_register.html")

@auth.route('/admin/remove_org')
def remove_organization():
    org_name = request.form.get('org-name')
    org_name_confirm = request.form.get('org-name-confirm')
    if org_name != org_name_confirm:
        flash("Organization names don't match. Try again")
        redirect(url_for('remove_organization.html'))
    else:
        existing_org = get_org_from_name(org_name)
        if existing_org == None:
            flash("No organization matching that name was returned", category='error')
        else:
            result = mongo_client.volunteer_connect.organization.delete_one({'name': org_name})
            if result > 0:
                flash('Successfully removed organization', category='success')
    return render_template('remove_organization.html')

@auth.route('/organizations', methods=['GET'])
def get_organizations():
    organizations_list = mongo_client.volunteer_connect.organization.find()
    print("organization list:::", organizations_list)
    return render_template('organization.html',organizations=organizations_list )


#helper_function
def get_org_from_name(org_name):
    return mongo_client.volunteer_connect.organization.find({"name":org_name})