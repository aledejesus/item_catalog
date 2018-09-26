from copy import copy
from flask import (
    Blueprint, render_template, abort, jsonify, request,
    redirect, url_for)
from sqlalchemy.orm import joinedload

from catalog import db
from .models import Item
from .forms import ItemForm

items_bp = Blueprint('items', __name__)


@items_bp.route('/<int:iid>')
def details(iid):
    item = Item.query.options(joinedload(Item.category)).get(iid)

    if item:
        return render_template('items/details.html', item=item)
    else:
        abort(404)


@items_bp.route('/<int:iid>/json')
def details_json(iid):
    item = Item.query.options(joinedload(Item.category)).get(iid)

    if item:
        return jsonify({'item': item.serialize()})
    else:
        abort(404)


@items_bp.route('/add/', methods=('GET', 'POST'))
def add():
    try:
        cid = int(request.args.get('cid'))
    except Exception as e:
        print(e)
        return redirect(url_for('categories.index'))
        # TODO: FLASH MESSAGE STATING PROBLEM

    form = ItemForm()
    form.category_id.data = cid

    if form.validate_on_submit():
        try:
            item_props = copy(form.data)
            del item_props['csrf_token']
            item = Item(**item_props)
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            print(e)
            # TODO: FLASH MESSAGE STATING PROBLEM
        else:
            # TODO: FLASH CREATION SUCCESS MESSAGE
            return redirect(url_for('items.details', iid=item.id))
    return render_template('items/add.html', form=form)
