from flask import Blueprint, render_template, abort
from sqlalchemy.orm import joinedload
from .models import Item

items_bp = Blueprint('items', __name__)


@items_bp.route('/<int:iid>')
def details(iid):
    item = Item.query.options(joinedload(Item.category)).get(iid)

    if item:
        return render_template('items/details.html', item=item)
    else:
        abort(404)
