from flask import Blueprint, redirect, url_for


users_bp = Blueprint('users', __name__)


@users_bp.route('/')
def home():
    return redirect(url_for('categories.index'))
