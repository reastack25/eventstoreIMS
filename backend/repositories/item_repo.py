# repositories/item_repo.py

from models.item import Item
from extensions import db

class ItemRepository:

    @staticmethod
    def get_all_paginated(page=1, per_page=20,search=None):

        query = Item.query

        if search:
            query = query.filter(
                Item.name.ilike(f"%{search}%")
            )
        return Item.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )