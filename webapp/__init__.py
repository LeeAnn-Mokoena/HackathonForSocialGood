from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']  = os.getenv("SECRET_KEY")

    from .routes.auth import auth , main
    from .routes.dashboard_main import dashboard
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(dashboard)
    return app