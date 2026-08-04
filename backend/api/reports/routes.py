from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from services.report_service import ReportService

reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/dashboard")

@reports_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    data = ReportService.get_dashboard_summary()
    return jsonify(data), 200

@reports_bp.route("/weekly", methods=["GET"])
@jwt_required()
def weekly_report():
    data = ReportService.get_weekly_report()
    return jsonify(data), 200

@reports_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_report():
    data = ReportService.get_monthly_report()
    return jsonify(data), 200

@reports_bp.route("/export/inventory", methods=["GET"])
@jwt_required()
def export_inventory():
    csv_data = ReportService.export_inventory_csv()
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=inventory.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@reports_bp.route("/export/damages", methods=["GET"])
@jwt_required()
def export_damages():
    csv_data = ReportService.export_damages_csv()
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=damages.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
