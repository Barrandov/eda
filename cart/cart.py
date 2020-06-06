from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from eda.models import Order, Meal, db
from eda.forms import BookingForm

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('', methods=['GET', 'POST'])
def cart_render():
    form = BookingForm()
    cart_items = {}
    total = 0

    if request.method == 'POST':
        if form.validate_on_submit():
            request_data = {'name': form.name.data,
                            'address': form.address.data,
                            'email': form.email.data,
                            'phone': form.phone.data,
                            'order_summ': form.order_summ.data,
                            'order_cart': form.order_cart.data
                            }

            request_to_db = Order(date='today',
                                  total=request_data['order_summ'],
                                  status='Pending',
                                  phone=request_data['phone'],
                                  address=request_data['address'],
                                  user_id=None
                                  )

            db.session.add(request_to_db)

            for i in request_data['order_cart'][1:-1].split(','):
                meal = db.session.query(Meal).get(int(i))
                request_to_db.meals_list.append(meal)

            db.session.commit()
            session['order'] = request_to_db.id
            return redirect(url_for('cart.ordered_render'))

    if not session.get('cart') is None:
        cart = db.session.query(Meal).filter(Meal.id.in_(session['cart']))

        for id in session['cart']:
            item = cart.filter(Meal.id == id).first()
            total += item.price
            if not id in cart_items:
                cart_items[item.id] = [item.title, item.price, 1]
            else:
                cart_items[item.id][2] += 1

    final_total = lambda sum: str(f'{sum:,}').replace(',', ' ')
    return render_template('cart.html', form=form, cart_items=cart_items, total=total, total_cool=final_total(total))


@cart.route('/delete/<int:id>/')
def cart_delete_render(id):

    if not session.get('cart') is None and id in session.get('cart'):

        tmp = session['cart']
        tmp.remove(id)
        session['cart'] = tmp

        flash(db.session.query(Meal).get(id).title, 'delete')

    return redirect(request.referrer)


@cart.route('/add/<int:id>/')
def add_render(id):
    meal_by_id = db.session.query(Meal).get_or_404(id)
    cart_session = session.get('cart', [])
    cart_session.append(meal_by_id.id)
    session['cart'] = cart_session
    flash(meal_by_id.title, 'add')

    return redirect(request.referrer)


@cart.route('/ordered/')
def ordered_render():
    if not session.get('order') is None:
        id = session['order']
        session.pop('order')
        return render_template('ordered.html', id=id)
    return 'Может все таки заказик сначала?'