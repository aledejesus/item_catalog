from flask import (
    Blueprint, redirect, url_for, session, render_template,
    request, current_app, flash)
from google.oauth2 import id_token
from google.auth.transport import requests
from catalog.utils import gen_ran_str

users_bp = Blueprint('users', __name__)


@users_bp.route('/')
def home():
    return redirect(url_for('categories.index'))


@users_bp.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session['state'] = gen_ran_str(32)
        return render_template('users/login.html')
    else:
        token = request.args.get('id_token', None)
        if token:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(),
                current_app.config['GOOGLE_CLIENT_ID'])

            if id_info['iss'] not in [
                    'accounts.google.com',
                    'https://accounts.google.com']:
                flash("Invalid token issuer", 'error')
                return render_template('users/login.html')

            g_user_id = id_info['sub']
            # TODO: ADD THIS PROPERTY TO THE APP USER MODEL
            # TODO: GET OTHER USER PROPERTIES FROM TOKEN PAYLOAD
            # TODO: CHECK NEXT STEPS IN UDACITY TUTORIAL
            # TODO: CREATE USER IF DOES NOT EXIST IN DB
            # TODO: LOGIN USER IF IT ALREADY EXISTS
            # TODO: TEST

        else:
            # TODO: COMPLETE
            pass
