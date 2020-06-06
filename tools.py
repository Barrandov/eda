import json

from models import *


def open_json(file):
    with open(f'tmp/{file}.json', 'r') as f:
        return json.load(f)


def convert_category():
    all_data = open_json('category')

    for data in all_data:
        row = Category(id=data['id'], title=data['title'])
        db.session.add(row)
    db.session.commit()


def convert_meal():
    all_data = open_json('meals')

    for data in all_data:
        row = Meal(title=data['title'],
                   price=data['price'],
                   pic=data['picture'],
                   desc=data['description'],
                   category_id=data['category_id'])

        db.session.add(row)

    db.session.commit()


convert_category()
convert_meal()
