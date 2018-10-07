from flask import (
    Blueprint, redirect, url_for, session, render_template,
    request, current_app, flash, abort, jsonify)
from google.oauth2 import id_token
from google.auth.transport import requests

from catalog import db
from .models import AppUser

users_bp = Blueprint('users', __name__)


@users_bp.route('/')
def home():
    """
    Get home page

    Arguments:
        None

    Returns:
        - redirection to categories index
    """
    return redirect(url_for('categories.index'))


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Render login page or try to log in depending on HTTP
    method used.

    Arguments:
        None

    Returns:
        - redirection to home on successful login
                OR
        - rendered login page on GET request, token
            issuer error detected, on user creation
            error or missing Google token
                OR
        - json object response with redirection path
            on successful login. This is done this
            way because the POST request of this
            endpoint is made using JavaScript
    """
    if session.get('app_user_id'):
        # redirect to home if already logged in
        flash("You are already logged in", 'info')
        return redirect(url_for('users.home'))
    elif request.method == 'GET':
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
                try:
                    app_user = AppUser(
                        google_id=id_info['sub'], name=id_info['name'],
                        email=id_info['email'])
                    db.session.add(app_user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("An error occurred. Try again later", 'error')
                    return render_template('users/login.html')

            session['app_user_id'] = app_user.id
            session['app_user_name'] = app_user.name
            session['app_user_email'] = app_user.email

            flash("Logged in successfully. Welcome {}".format(
                app_user.name), 'info')
            return jsonify({'next': url_for('users.home')})

        else:
            flash("Google token missing. Try again later", 'error')
            return render_template('users/login.html')


@users_bp.route('/logout', methods=['POST'])
def logout():
    """
    Log user out

    Arguments:
        None

    Returns:
        - json response with redirection URL. This is done
            this way because the POST request of this
            endpoint is made using JavaScript

    Raises:
        - flask.HTTPException if user is not logged in
    """
    if session.get('app_user_id'):
        del session['app_user_id']
        del session['app_user_name']
        del session['app_user_email']

        flash("You have logged out", 'info')
        return jsonify({'next': url_for("users.login")})
    else:
        flash("Log out failed. You are not logged in")
        abort(400)
