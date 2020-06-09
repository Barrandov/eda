from flask import Blueprint, render_template, session
from models import Category, db



index = Blueprint('index', __name__, template_folder='templates')


@index.route('')
def index_render():
    print(session)
    category = db.session.query(Category).all()
    return render_template('index.html', category=category)