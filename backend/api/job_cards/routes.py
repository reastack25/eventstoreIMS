
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.job_card_service import JobCardService

job_cards_bp = Blueprint(
    "job_cards",
    __name__,
    url_prefix="/api/v1/job-cards"
)


@job_cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_job_card():
    data       = request.get_json()
    created_by = get_jwt_identity()

    if not data.get("event_id"):
        return jsonify({"error": "event_id is required"}), 422

    if not data.get("items"):
        return jsonify({"error": "At least one item is required"}), 422

    job_card = JobCardService.create(data, created_by)

    return jsonify({
        "message":  "Job card created",
        "job_card": job_card.to_dict()
    }), 201


@job_cards_bp.route("/", methods=["GET"])
@jwt_required()
def list_job_cards():
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = JobCardService.get_all(page, per_page)

    return jsonify({
        "job_cards": [jc.to_dict() for jc in pagination.items],
        "meta": {
            "page":        pagination.page,
            "per_page":    pagination.per_page,
            "total":       pagination.total,
            "total_pages": pagination.pages
        }
    }), 200


@job_cards_bp.route("/<int:job_card_id>", methods=["GET"])
@jwt_required()
def get_job_card(job_card_id):
    job_card = JobCardService.get_one(job_card_id)
    return jsonify(job_card.to_dict()), 200


@job_cards_bp.route("/<int:job_card_id>/dispatch", methods=["POST"])
@jwt_required()
def dispatch_job_card(job_card_id):
    performed_by = get_jwt_identity()

    try:
        job_card = JobCardService.dispatch(job_card_id, performed_by)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({
        "message":  "Job card dispatched",
        "job_card": job_card.to_dict()
    }), 200


@job_cards_bp.route("/<int:job_card_id>/return", methods=["POST"])
@jwt_required()
def return_job_card(job_card_id):
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("returns"):
        return jsonify({"error": "returns list is required"}), 422

    try:
        job_card = JobCardService.return_items(
            job_card_id,
            data["returns"],
            performed_by
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({
        "message":  "Items returned successfully",
        "job_card": job_card.to_dict()
    }), 200