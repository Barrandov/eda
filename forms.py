from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField, FieldList
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired()])
    address = StringField('Адрес', [InputRequired()])
    email = StringField('Email', [InputRequired()])
    phone = StringField('Телефон', [Length(min=5, message='Телефон слишком короткий')])

    order_summ = HiddenField('order_summ')
    order_cart = HiddenField('order_cart')


class RegistrationForm(FlaskForm):
    email = StringField('Email', [InputRequired()])
    password = StringField('Password', [InputRequired()])
