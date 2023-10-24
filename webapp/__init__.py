from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    #app instance
    app = Flask(__name__)
    app.config['SECRET_KEY']  = os.getenv("SECRET_KEY")

    from .routes.auth import auth as user_auth, main
    from .routes.organizations import v_opportunities
    from .routes.dashboard_main import dashboard
    
    app.register_blueprint(user_auth)
    app.register_blueprint(main)
    app.register_blueprint(dashboard)
    app.register_blueprint(v_opportunities, url_prefix='/')

    print('app started::')
    return app