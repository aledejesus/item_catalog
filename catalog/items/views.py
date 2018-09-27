from copy import copy
from flask import (
    Blueprint, render_template, abort, jsonify, request,
    redirect, url_for, flash)
from sqlalchemy.orm import joinedload

from catalog import db
from catalog.categories.models import Category
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
    cid = ''
    try:
        cid = int(request.args.get('cid'))
        Category.query.filter_by(id=cid).one()
    except Exception as e:
        print(e)
        flash("Invalid category id ({})".format(cid), 'error')
        return redirect(url_for('categories.index'))

    form = ItemForm()
    form.category_id.data = cid

    if form.validate_on_submit():
        item_props = copy(form.data)
        del item_props['csrf_token']

        item = Item.query.filter_by(name=item_props['name']).first()
        if item:
            flash("name: Item with name '{}' already exists".format(
                item_props['name']), 'error')
            return render_template('items/add.html', form=form)

        try:
            item = Item(**item_props)
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("An error ocurred while creating the item", 'error')
        else:
            flash("Item created successfully", 'info')
            return redirect(url_for('items.details', iid=item.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}: {}".format(field, error), 'error')

    return render_template('items/add.html', form=form)
