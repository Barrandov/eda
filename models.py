from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore

db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref='user',)
    orders = db.relationship('Order', backref='user')

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


meal_order_asso = db.Table(
    'meal_order_asso',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id', ondelete='CASCADE')),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id', ondelete='CASCADE')),
)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    total = db.Column(db.Integer)
    status = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)

    meals_list = db.relationship('Meal', secondary=meal_order_asso, backref='order')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    meals = db.relationship('Meal', backref='category')


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Integer)
    desc = db.Column(db.String)
    pic = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))





