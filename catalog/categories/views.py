from flask import Blueprint, render_template, abort, session
from sqlalchemy.orm import joinedload
from .models import Category

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)


@categories_bp.route('/<int:cid>')
def details(cid):
    category = Category.query.options(joinedload(Category.items)).get(cid)
    can_create_item = bool(session.get('app_user_id', ''))
    if category:
        return render_template(
            'categories/details.html', category=category,
            can_create_item=can_create_item)
    else:
        abort(404)
