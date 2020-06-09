from flask import Flask, session, redirect, url_for, request
from flask_migrate import Migrate
from flask_security import Security, user_registered, current_user
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView

from models import *
from config import Config

from index.index import index
from cart.cart import cart
from account.account import account

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)



class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Order, db.session))
admin.add_view(AdminView(Meal, db.session))
admin.add_view(AdminView(Category, db.session))



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
