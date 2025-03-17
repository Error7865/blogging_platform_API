from flask import Blueprint, g
from flask_httpauth import HTTPBasicAuth
from app.data import User

api = Blueprint('api', __name__, url_prefix='/api')

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    # u = User(email=email)
    # print('Here was email ', u.verify_password('richi'))
    try:
        user = User(email=email)
        g.current_user = user
        # print('Here check user password ', user.verify_password(password))
    except ValueError as e:
        return False
    try:
        return user.verify_password(password)
    except AttributeError as e: #for new user they have not any id which cause an error
        return False

from . import calls