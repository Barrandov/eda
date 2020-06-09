from flask import Flask, session
from flask_migrate import Migrate
from flask_security import Security, user_registered, current_user

from models import *
from config import Config

from index.index import index
from cart.cart import cart
from account.account import account

app = Flask(__name__)
app.config.from_object(Config)

app.config['SECURITY_SEND_REGISTER_EMAIL'] = False


db.init_app(app)
migrate = Migrate(app, db)

security = Security(app, user_datastore)

app.register_blueprint(index, url_prefix='/')
app.register_blueprint(cart, url_prefix='/cart/')
app.register_blueprint(account, url_prefix='/account/')



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


@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()



app.run('0.0.0.0', debug=True)
