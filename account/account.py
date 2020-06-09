from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_security import current_user, roles_required

from models import Order, Meal, db, User


account = Blueprint('account', __name__, template_folder='templates')


@account.route('', methods=['GET', 'POST'])
def account_render():

    user = db.session.query(User).get(current_user.id)

    if user.orders:
        order_list = []
        for order in user.orders:
            elem = {'order_id': order.id, 'order_total': order.total, 'order_date': order.date}
            elem['meals_list'] = []
            for meal in order.meals_list:
                elem['meals_list'].append({'id':meal.id, 'title': meal.title, 'price': meal.price})
            order_list.append(elem)

    return render_template('account.html', order_list=order_list)