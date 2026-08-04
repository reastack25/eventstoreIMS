from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.user import User
from models.job_card import JobCard
from models.damage_log import DamageLog
from extensions import db

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.filter_by(is_active=True).all()
    result = []
    for user in users:
        # Count job cards assigned
        job_cards = JobCard.query.filter_by(created_by=user.id).all()
        dispatched = [jc for jc in job_cards if jc.status == "DISPATCHED"]
        returned   = [jc for jc in job_cards if jc.status == "RETURNED"]

        # Count damages reported by user
        damages     = DamageLog.query.filter_by(reported_by=user.id).all()
        damage_cost = sum(d.estimated_cost or 0 for d in damages)

        result.append({
            "id":           user.id,
            "full_name":    user.full_name,
            "email":        user.email,
            "role":         user.role,
            "total_jobs":   len(job_cards),
            "dispatched":   len(dispatched),
            "returned":     len(returned),
            "damages":      len(damages),
            "damage_cost":  damage_cost,
            "recent_jobs":  [
                {
                    "reference":  jc.reference,
                    "event_name": jc.event.name if jc.event else None,
                    "status":     jc.status,
                    "created_at": jc.created_at.isoformat()
                }
                for jc in sorted(job_cards, key=lambda x: x.created_at, reverse=True)[:3]
            ]
        })

    return jsonify(result), 200
