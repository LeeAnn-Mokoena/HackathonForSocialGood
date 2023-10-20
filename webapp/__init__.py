from flask import Flask
from dotenv import load_dotenv, find_dotenv
from webapp.extensions import mongo_client
#from extensions import mongo_client
from flask import Blueprint, g, render_template, request, jsonify


#load_dotenv(find_dotenv())


def create_app(config_object='app.settings'):
    #app instance
    app = Flask(__name__)
    #app.config['PASSAGE_API_KEY'] = os.getenv("PASSAGE_API_KEY")
    #app.config['PASSAGE_APP_ID'] = os.getenv("PASSAGE_APP_ID")

    app.config.from_object(config_object)
    
    mongo_client.init_app(app)

    from .routes import user_auth
    
    app.register_blueprint(user_auth, url_prefix='/')

    print('app started::')
    return app
