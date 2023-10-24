from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import pprint
from pymongo import MongoClient

load_dotenv()

organizations = Blueprint('organizations', __name__)

mongo_client = MongoClient(os.getenv("MONGO_URI"))

@organizations.route('/organizations', methods=['GET'])
def get_organizations():
    organizations_list = mongo_client.volunteer_connect.organization.find()
    print("organization list:::", organizations_list)


@organizations.route('/organization/sign-up', methods=['GET', 'POST'])
def create_organization():
    return ""


@organizations.route('/organization/<str:orgId>/opportunities', methods=['GET', 'POST'])
def organization_opportunities(org_id):
    id_as_object = ObjectId(org_id)
    print("org id::::", id_as_object)
    org = mongo_client.volunteer_connect.organization.find_one({"_id": id_as_object})
    print('org:::::', org)


