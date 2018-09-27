from flask import Blueprint, render_template, abort
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

    if category:
        return render_template(
            'categories/details.html', category=category)
    else:
        abort(404)
