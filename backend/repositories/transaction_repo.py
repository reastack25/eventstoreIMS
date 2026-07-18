from extensions import db
from models.inventory_transaction import InventoryTransaction

class TransactionRepository:

    @staticmethod
    def create(transaction):
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_all():
        return InventoryTransaction.query.order_by(
            InventoryTransaction.created_at.desc()
        ).all()