from flask import Flask, render_template, request, redirect, session, flash
from flask_migrate import Migrate

from models import *
from forms import BookingForm

from index.index import index
from cart.cart import cart

app = Flask(__name__)
app.secret_key = "4iko42k24pk"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eda.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(index, url_prefix='/')
app.register_blueprint(cart, url_prefix='/cart/')



@app.context_processor
def menu_cart():
    if not session.get('cart') is None:
        cart = db.session.query(Meal).filter(Meal.id.in_(session['cart']))
        total = 0
        for id in session['cart']:
            total += cart.filter(Meal.id == id).first().price
        final_total = lambda sum: str(f'{sum:,}').replace(',', ' ')
        return dict(menu_cart=f'{len(session["cart"])} блюд, {final_total(total)} ₽')
    return dict(menu_cart='Пусто')
















app.run('0.0.0.0', debug=True)
