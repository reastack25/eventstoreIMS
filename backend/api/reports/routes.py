from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models.item import Item
from models.category import Category
from models.damage_log import DamageLog
from models.inventory_transaction import InventoryTransaction
from extensions import db

reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/v1/dashboard"
)

@reports_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():

    total_items      = Item.query.filter_by(status="ACTIVE").count()
    total_categories = Category.query.count()

    # Items where available stock is below 10
    low_stock        = Item.query.filter(Item.available < 10).count()

    # Total damaged quantity from damage logs
    damaged_items    = db.session.query(
        db.func.sum(DamageLog.quantity)
    ).scalar() or 0

    # Dispatched items with no matching return yet
    dispatched = db.session.query(
        db.func.sum(InventoryTransaction.quantity)
    ).filter_by(transaction_type="DISPATCH").scalar() or 0

    returned = db.session.query(
        db.func.sum(InventoryTransaction.quantity)
    ).filter_by(transaction_type="RETURN").scalar() or 0

    pending_returns = max(dispatched - returned, 0)

    return jsonify({
        "total_items":      total_items,
        "total_categories": total_categories,
        "low_stock":        low_stock,
        "damaged_items":    damaged_items,
        "pending_returns":  pending_returns
    }), 200