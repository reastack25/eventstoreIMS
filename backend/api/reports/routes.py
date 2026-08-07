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


@reports_bp.route("/export/pdf/weekly", methods=["GET"])
@jwt_required()
def export_weekly_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io
    from datetime import datetime

    data   = ReportService.get_weekly_report()
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story  = []

    # Title
    story.append(Paragraph("Elroyy Events — Weekly Report", styles["Title"]))
    story.append(Paragraph(data["period"], styles["Normal"]))
    story.append(Spacer(1, 20))

    # Table data
    table_data = [
        ["Metric", "Value"],
        ["Events Serviced",  str(data["events_serviced"])],
        ["Items Dispatched", str(data["items_dispatched"])],
        ["Items Returned",   str(data["items_returned"])],
        ["Shortfalls",       str(data["shortfalls"])],
        ["Damages Logged",   str(data["damages_logged"])],
        ["Est. Damage Cost", f"KES {data['damage_cost']:,.0f}"],
    ]

    table = Table(table_data, colWidths=[300, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a0a0a")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, 0), 11),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f8f8")]),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("FONTSIZE",   (0, 1), (-1, -1), 10),
        ("PADDING",    (0, 0), (-1, -1), 10),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        f"Generated on {datetime.utcnow().strftime('%d %b %Y %H:%M')} UTC",
        styles["Normal"]
    ))

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Type"]        = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=weekly-report.pdf"
    return response
