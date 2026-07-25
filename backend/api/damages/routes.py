from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.role_middleware import permission_required
from extensions import db
from models.damage_log import DamageLog
from models.item import Item
from models.inventory_transaction import InventoryTransaction
from models.audit_log import AuditLog

damages_bp = Blueprint("damages", __name__, url_prefix="/api/v1/damages")

@damages_bp.route("/", methods=["GET"])
@jwt_required()
def get_damages():
    damages = DamageLog.query.order_by(DamageLog.created_at.desc()).all()
    total_cost = sum(d.estimated_cost or 0 for d in damages)
    return jsonify({
        "damages":    [d.to_dict() for d in damages],
        "total_cost": total_cost,
        "count":      len(damages)
    }), 200


@damages_bp.route("/", methods=["POST"])
@jwt_required()
@permission_required("report_damage")
def report_damage():
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("item_id") or not data.get("quantity"):
        return jsonify({"error": "item_id and quantity are required"}), 422

    item = Item.query.get_or_404(data["item_id"])

    if item.available < data["quantity"]:
        return jsonify({
            "error": f"Cannot damage more than available. Available: {item.available}"
        }), 409

    # Reduce stock
    item.available -= data["quantity"]
    item.quantity  -= data["quantity"]

    # Create damage log
    damage = DamageLog(
        item_id        = item.id,
        quantity       = data["quantity"],
        reason         = data.get("reason"),
        reported_by    = performed_by,
        estimated_cost = data.get("estimated_cost", 0),
        job_card_ref   = data.get("job_card_ref")
    )
    db.session.add(damage)

    # Record transaction
    tx = InventoryTransaction(
        item_id          = item.id,
        transaction_type = "DAMAGE",
        quantity         = data["quantity"],
        performed_by     = performed_by,
        remarks          = data.get("reason")
    )
    db.session.add(tx)

    # Audit log
    log = AuditLog(
        user_id = performed_by,
        action  = "REPORT_DAMAGE",
        details = f"Reported {data['quantity']} damaged units of {item.name}. Reason: {data.get('reason')}"
    )
    db.session.add(log)

    db.session.commit()

    return jsonify({
        "message": "Damage reported successfully",
        "damage":  damage.to_dict()
    }), 201
