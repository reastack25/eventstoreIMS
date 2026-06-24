from models.item import Item
from extensions import db


class InventoryRepository:
    @staticmethod
    def get_all():
        return Item.query.all()

    @staticmethod
    def create(item):
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_by_id(item_id):
        return Item.query.get(item_id)