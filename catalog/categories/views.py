from flask import render_template, Blueprint


categories_bp = Blueprint('categories', __name__, template_folder='templates')


@categories_bp.route('/')
def index():
    return render_template('index.html')
