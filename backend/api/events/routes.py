
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.event import Event
from extensions import db

events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/api/v1/events"
)

@events_bp.route("/", methods=["POST"])
@jwt_required()
def create_event():
    data       = request.get_json()
    created_by = get_jwt_identity()

    if not data.get("name") or not data.get("event_date"):
        return jsonify({"error": "name and event_date are required"}), 422

    event = Event(
        name        = data["name"],
        client_name = data.get("client_name"),
        event_date  = data["event_date"],
        venue       = data.get("venue"),
        status      = "UPCOMING",
        created_by  = created_by
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({
        "message": "Event created",
        "event":   event.to_dict()
    }), 201


@events_bp.route("/", methods=["GET"])
@jwt_required()
def list_events():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return jsonify([e.to_dict() for e in events]), 200


@events_bp.route("/<int:event_id>", methods=["GET"])
@jwt_required()
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict()), 200