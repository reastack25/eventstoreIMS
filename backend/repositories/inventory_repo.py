from models.item import Item
from extensions import db

class ItemRepository:

    @staticmethod
    def get_all_paginated(page=1, per_page=20, search=None):
        query = Item.query

        if search:
            query = query.filter(
                Item.name.ilike(f"%{search}%")
            )

        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def get_by_id(item_id):
        return Item.query.get(item_id)

    @staticmethod
    def create(item):
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_all():
        return Item.query.all()
