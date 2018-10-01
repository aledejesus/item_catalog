from flask import (
    Blueprint, redirect, url_for, session, render_template,
    request, current_app, flash)
from google.oauth2 import id_token
from google.auth.transport import requests

from catalog import db
from catalog.utils import gen_ran_str
from .models import AppUser

users_bp = Blueprint('users', __name__)


@users_bp.route('/')
def home():
    return redirect(url_for('categories.index'))


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    # redirect to home if already loged in
    if session.get('app_user_id'):
        flash("You are already logged in", 'info')
        return redirect(url_for('users.home'))
    if request.method == 'GET':
        session['state'] = gen_ran_str(32)
        return render_template('users/login.html')
    else:
        token = request.form.get('id_token', None)
        if token:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(),
                current_app.config['GOOGLE_CLIENT_ID'])

            if id_info['iss'] not in [
                    'accounts.google.com',
                    'https://accounts.google.com']:
                flash("Invalid token issuer", 'error')
                return render_template('users/login.html')

            app_user = AppUser.query.filter_by(
                google_id=id_info['sub']).first()

            if not app_user:
                app_user = AppUser(
                    google_id=id_info['sub'], name=id_info['name'],
                    email=id_info['email'])
                db.session.add(app_user)
                db.session.commit()

            session['app_user_id'] = app_user.id
            session['app_user_name'] = app_user.name
            session['app_user_email'] = app_user.email

            flash("Logged in successfully. Welcome {}".format(
                app_user.name), 'info')
            return redirect(url_for('users.home'))

        else:
            flash("Google token missing. Try again later", 'error')
            return render_template('users/login.html')
