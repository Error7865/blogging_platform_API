from flask import Flask
from redis import Redis
from dotenv import load_dotenv
import os
from config import config


load_dotenv() # load environment variables

con = Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'),
             db=os.environ['DB'], decode_responses = True)

def crate_app(config_name:str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # register blueprints here
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint)
    return app

