from flask import Blueprint
from flask import jsonify
from flask import request

from services.inventory_service import InventoryService
from schemas.inventory_schema import ItemSchema

inventory_bp = Blueprint("inventory", __name__,url_prefix="/api/v1/inventory")

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# @inventory_bp.route("//")
# def health():
#     return {
#         "module": "inventory",
#         "status": "running"
#     }

@inventory_bp.route("/", methods=["POST"])
def create_item():

    data = request.get_json()
    item = InventoryService.create_item(data)
    return (
        item_schema.dump(item),201
    )

@inventory_bp.route("/", methods=["GET"])
def get_inventory():

    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    per_page = min(per_page, 100)

    pagination = ItemRepository.get_all_paginated(page, per_page)

    return jsonify({
        "items": [item.to_dict() for item in pagination.items],
        "meta": {
            "page":        pagination.page,
            "per_page":    pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "has_next":    pagination.has_next,
            "has_prev":    pagination.has_prev
        }
    }), 200