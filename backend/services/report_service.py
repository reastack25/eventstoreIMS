from extensions import db
from models.item import Item
from models.event import Event
from models.job_card import JobCard
from models.job_card_item import JobCardItem
from models.damage_log import DamageLog
from models.inventory_transaction import InventoryTransaction
from datetime import datetime, timedelta
import csv
import io

class ReportService:

    @staticmethod
    def get_dashboard_summary():
        from models.category import Category

        total_items      = Item.query.filter_by(status="ACTIVE").count()
        total_categories = Category.query.count()
        low_stock        = Item.query.filter(Item.available < 10).count()

        damaged_items = db.session.query(
            db.func.coalesce(db.func.sum(DamageLog.quantity), 0)
        ).scalar()

        # Items currently out — dispatched but not returned
        dispatched = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter_by(transaction_type="DISPATCH").scalar()

        returned = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter_by(transaction_type="RETURN").scalar()

        items_out = max(int(dispatched) - int(returned), 0)

        # Active events
        active_events = Event.query.filter_by(status="UPCOMING").count()

        # Pending returns — dispatched job cards
        pending_returns = JobCard.query.filter_by(status="DISPATCHED").count()

        return {
            "total_items":      total_items,
            "total_categories": total_categories,
            "low_stock":        low_stock,
            "damaged_items":    int(damaged_items),
            "items_out":        items_out,
            "active_events":    active_events,
            "pending_returns":  pending_returns,
        }

    @staticmethod
    def get_weekly_report():
        week_ago = datetime.utcnow() - timedelta(days=7)

        events_this_week = Event.query.filter(
            Event.created_at >= week_ago
        ).count()

        dispatched = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter(
            InventoryTransaction.transaction_type == "DISPATCH",
            InventoryTransaction.created_at >= week_ago
        ).scalar()

        returned = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter(
            InventoryTransaction.transaction_type == "RETURN",
            InventoryTransaction.created_at >= week_ago
        ).scalar()

        damages = DamageLog.query.filter(
            DamageLog.created_at >= week_ago
        ).all()

        damage_cost = sum(d.estimated_cost or 0 for d in damages)

        return {
            "period":           f"{week_ago.strftime('%d %b')} – {datetime.utcnow().strftime('%d %b %Y')}",
            "events_serviced":  events_this_week,
            "items_dispatched": int(dispatched),
            "items_returned":   int(returned),
            "shortfalls":       max(int(dispatched) - int(returned), 0),
            "damages_logged":   len(damages),
            "damage_cost":      damage_cost,
        }

    @staticmethod
    def get_monthly_report():
        month_ago = datetime.utcnow() - timedelta(days=30)

        events = Event.query.filter(Event.created_at >= month_ago).count()

        dispatched = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter(
            InventoryTransaction.transaction_type == "DISPATCH",
            InventoryTransaction.created_at >= month_ago
        ).scalar()

        returned = db.session.query(
            db.func.coalesce(db.func.sum(InventoryTransaction.quantity), 0)
        ).filter(
            InventoryTransaction.transaction_type == "RETURN",
            InventoryTransaction.created_at >= month_ago
        ).scalar()

        dispatched_int = int(dispatched)
        returned_int   = int(returned)
        return_rate    = round((returned_int / dispatched_int * 100), 1) if dispatched_int > 0 else 0

        damages = DamageLog.query.filter(DamageLog.created_at >= month_ago).all()
        damage_cost = sum(d.estimated_cost or 0 for d in damages)

        # Top 5 most used items
        top_items = db.session.query(
            Item.name,
            db.func.sum(InventoryTransaction.quantity).label("total")
        ).join(InventoryTransaction, Item.id == InventoryTransaction.item_id)\
         .filter(
             InventoryTransaction.transaction_type == "DISPATCH",
             InventoryTransaction.created_at >= month_ago
         ).group_by(Item.id)\
          .order_by(db.text("total DESC"))\
          .limit(5).all()

        return {
            "period":          f"Last 30 days",
            "total_events":    events,
            "items_moved":     dispatched_int,
            "return_rate":     return_rate,
            "damage_incidents":len(damages),
            "damage_cost":     damage_cost,
            "top_items":       [{"name": r[0], "total": int(r[1])} for r in top_items],
        }

    @staticmethod
    def export_inventory_csv():
        items = Item.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Code", "Name", "Unit", "Quantity", "Available", "Status"])
        for item in items:
            writer.writerow([
                item.code, item.name, item.unit,
                item.quantity, item.available, item.status
            ])
        return output.getvalue()

    @staticmethod
    def export_damages_csv():
        damages = DamageLog.query.order_by(DamageLog.created_at.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Item", "Code", "Quantity", "Reason", "Job Card", "Est. Cost (KES)", "Reported By"])
        for d in damages:
            writer.writerow([
                d.created_at.strftime("%Y-%m-%d"),
                d.item.name if d.item else "",
                d.item.code if d.item else "",
                d.quantity,
                d.reason or "",
                d.job_card_ref or "",
                d.estimated_cost or 0,
                d.reporter.full_name if d.reporter else ""
            ])
        return output.getvalue()
