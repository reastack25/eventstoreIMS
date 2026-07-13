
from extensions import db
from models.job_card import JobCard
from models.job_card_item import JobCardItem
from models.event import Event
from services.inventory_service import InventoryService

class JobCardService:

    @staticmethod
    def _generate_reference():
        last = JobCard.query.order_by(JobCard.id.desc()).first()
        next_id = (last.id + 1) if last else 1
        return f"JC-{str(next_id).zfill(3)}"  # JC-001, JC-002...

    @staticmethod
    def create(data, created_by):
        event = Event.query.get_or_404(data["event_id"])

        job_card = JobCard(
            reference  = JobCardService._generate_reference(),
            event_id   = event.id,
            assigned_to = data.get("assigned_to"),
            notes      = data.get("notes"),
            status     = "DRAFT",
            created_by = created_by
        )
        db.session.add(job_card)
        db.session.flush()  # get the id before commit

        # Add items to the job card
        for item_data in data.get("items", []):
            jc_item = JobCardItem(
                job_card_id        = job_card.id,
                item_id            = item_data["item_id"],
                quantity_requested = item_data["quantity"]
            )
            db.session.add(jc_item)

        db.session.commit()
        return job_card

    # ── DISPATCH JOB CARD ────────────────────────────────────
    @staticmethod
    def dispatch(job_card_id, performed_by):
        job_card = JobCard.query.get_or_404(job_card_id)

        if job_card.status != "DRAFT":
            raise ValueError(f"Job card is already {job_card.status}")

        # Dispatch each item
        for jc_item in job_card.items:
            InventoryService.dispatch_stock({
                "item_id":  jc_item.item_id,
                "quantity": jc_item.quantity_requested,
                "job_card": job_card.reference,
                "remarks":  f"Dispatched for {job_card.reference}"
            }, performed_by)

        job_card.status = "DISPATCHED"
        db.session.commit()
        return job_card

    # ── RETURN JOB CARD ──────────────────────────────────────
    @staticmethod
    def return_items(job_card_id, returns, performed_by):
        """
        returns = [
            {"item_id": 1, "quantity_returned": 8, "quantity_damaged": 2}
        ]
        """
        job_card = JobCard.query.get_or_404(job_card_id)

        if job_card.status != "DISPATCHED":
            raise ValueError("Can only return items from a dispatched job card")

        for ret in returns:
            jc_item = JobCardItem.query.filter_by(
                job_card_id = job_card_id,
                item_id     = ret["item_id"]
            ).first_or_404()

            qty_returned = ret.get("quantity_returned", 0)
            qty_damaged  = ret.get("quantity_damaged", 0)

            # Return good stock
            if qty_returned > 0:
                InventoryService.return_stock({
                    "item_id":  ret["item_id"],
                    "quantity": qty_returned,
                    "job_card": job_card.reference
                }, performed_by)

            # Report damaged stock
            if qty_damaged > 0:
                InventoryService.report_damage({
                    "item_id":  ret["item_id"],
                    "quantity": qty_damaged,
                    "reason":   f"Damaged on return from {job_card.reference}"
                }, performed_by)

            jc_item.quantity_returned = qty_returned
            jc_item.quantity_damaged  = qty_damaged

        job_card.status = "RETURNED"
        db.session.commit()
        return job_card

    @staticmethod
    def get_all(page=1, per_page=20):
        return JobCard.query.order_by(
            JobCard.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_one(job_card_id):
        return JobCard.query.get_or_404(job_card_id)