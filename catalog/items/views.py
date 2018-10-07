from copy import copy
from flask import (
    Blueprint, render_template, abort, jsonify, request,
    redirect, url_for, flash, session)
from sqlalchemy import and_, not_
from sqlalchemy.orm import joinedload

from catalog import db
from catalog.categories.models import Category
from .models import Item
from .forms import ItemForm, DeleteItemForm

items_bp = Blueprint('items', __name__)


@items_bp.route('/<int:iid>')
def details(iid):
    """
    Render Item details

    Arguments:
        - iid (int): item id

    Returns:
        - string: rendered HTML template

    Raises:
        - flask.HTTPException on inexistent Item
    """
    item = Item.query.options(joinedload(Item.category)).get(iid)
    delete_form = DeleteItemForm()
    app_user_id = session.get('app_user_id', '')
    can_modify_item = app_user_id and (item.app_user_id == app_user_id)

    if item:
        return render_template(
            'items/details.html', item=item, delete_form=delete_form,
            can_modify_item=can_modify_item)
    else:
        abort(404)


@items_bp.route('/<int:iid>/json')
def details_json(iid):
    """
    Get Item details in json format

    Arguments:
        - iid (int): item id

    Returns:
        - json object with Item properties

    Raises:
        - flask.HTTPException on inexistent Item
    """
    item = Item.query.options(joinedload(Item.category)).get(iid)

    if item:
        return jsonify({'item': item.serialize()})
    else:
        abort(404)


@items_bp.route('/add/', methods=('GET', 'POST'))
def add():
    """
    Add Item to the Category specified in the query string

    Arguments:
        None

    Returns:
        - redirection to /categories when there's an error
            in the cid parameter or item is successfully created
                OR
        - rendered /items/add HTML template when there
            errors occurred while creating the Item
    """
    # check that a user is logged in
    app_user_id = session.get('app_user_id', '')
    if not app_user_id:
        flash("Log in to create items", 'error')
        return redirect(url_for('categories.index'))

    # verify that category id is in URL and that category exists
    cid = ''
    try:
        cid = int(request.args.get('cid'))
        category = Category.query.filter_by(id=cid).one()
    except Exception as e:
        print(e)
        flash("Invalid category id ({})".format(cid), 'error')
        return redirect(url_for('categories.index'))

    # create form
    form = ItemForm()
    form.category_id.data = cid

    # validate form if POST request
    if form.validate_on_submit():
        # get item properties
        item_props = copy(form.data)
        del item_props['csrf_token']
        item_props['app_user_id'] = app_user_id

        # check that item with same name does not exist
        item = Item.query.filter_by(name=item_props['name']).first()
        if item:
            flash("name: Item with name '{}' already exists".format(
                item_props['name']), 'error')
            return render_template(
                'items/add.html', form=form, category=category)

        # create item
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
        # flash form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}: {}".format(field, error), 'error')

    return render_template('items/add.html', form=form, category=category)


@items_bp.route('/edit/<int:iid>', methods=('GET', 'POST'))
def edit(iid):
    """
    Update item with id specified in request path

    Arguments:
        - iid (int): Item id

    Returns:
        - redirection to /categories when item does not exist
                OR
        - redirection to item details page when user is not the
            creator of the item
                OR
        - redirection to item edit page when there are form errors
                OR
        - redirection to item details page on successful update
                OR
        - rendered item edit HTML template when errors
            occurred while modifying the Item
    """
    # check item existence
    try:
        item = Item.query.filter_by(id=iid).one()
    except Exception as e:
        print(e)
        flash("Item with id ({}) does not exist".format(iid), 'error')
        return redirect(url_for('categories.index'))

    # check that logged in user is the creator of the item
    app_user_id = session.get('app_user_id', '')
    if not (app_user_id and (item.app_user_id == app_user_id)):
        flash("You can't edit this item. You are not its creator", 'error')
        return redirect(url_for('items.details', iid=iid))

    # create form
    form = ItemForm(obj=item)

    # validate form if POST request
    if form.validate_on_submit():
        # check name duplicity
        same_name_item = Item.query.filter(
            and_(Item.name == form.name.data,
                 not_(Item.id == item.id))).first()
        if same_name_item:
            flash("name: Item with name '{}' already exists".format(
                form.name.data), 'error')
            return render_template('items/edit.html', form=form, item=item)

        # validate category exists
        category = Category.query.get(form.category_id.data)
        if not category:
            flash("category_id: Category with id ({}) does not exist".format(
                form.category_id.data), 'error')
            return render_template('items/edit.html', form=form, item=item)

        # modify item
        try:
            for k, v in form.data.items():
                if hasattr(item, k):
                    setattr(item, k, v)
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("An error occurred while modifying item", 'error')
        else:
            flash("Item modified successfully", 'info')
            return redirect(url_for('items.details', iid=item.id))
    else:
        # flash form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}: {}".format(field, error), 'error')

    return render_template('items/edit.html', form=form, item=item)


@items_bp.route('/delete/<int:iid>', methods=('POST',))
def delete(iid):
    """
    Delete item with id specified in request path

    Arguments:
        - iid (int): Item id

    Returns:
        - redirection to /categories when item does not exist
                OR
        - redirection to item details page when user is not the
            creator of the item
                OR
        - redirection to category details page on successful deletion
    """
    # create form
    form = DeleteItemForm()

    # validate form if POST request
    if form.validate_on_submit():
        item = Item.query.get(iid)

        if item:
            # check that logged in user is the creator of the item
            app_user_id = session.get('app_user_id', '')
            if not (app_user_id and (item.app_user_id == app_user_id)):
                flash(
                    "You can't delete this item. "
                    "You are not its creator", 'error')
                return redirect(url_for('items.details', iid=iid))

            # delete item
            try:
                db.session.delete(item)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("An error occurred while deleting item", 'error')
            else:
                flash("Item successfully deleted", 'info')
        else:
            flash("Item with id ({}) does not exist".format(iid), 'error')
            return redirect(url_for('categories.index'))
    else:
        # flash form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}: {}".format(field, error), 'error')

    return redirect(url_for('categories.details', cid=item.category_id))
