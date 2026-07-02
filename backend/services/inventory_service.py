from repositories.inventory_repo import InventoryRepository
from models.item import Item

class InventoryService:

    @staticmethod
    def create_item(data):

        item = Item(
            code=data["code"],
            name=data["name"],
            quantity=data.get("quantity", 0),
            available=data.get("available", 0),
            status=data.get("status", "ACTIVE"),
            category_id=data["category_id"]
        )
        return InventoryRepository.create(item)

    @staticmethod
    def get_items():
        return InventoryRepository.get_all()


    @staticmethod
    def _record_transaction(item_id, transaction_type, quantity, performed_by, reference_number=None, remarks=None):
        tx = InventoryTransaction(
            item_id          = item_id,
            transaction_type = transaction_type,
            quantity         = quantity,
            reference_number = reference_number,
            remarks          = remarks,
            performed_by     = performed_by
        )
        db.session.add(tx)
        return tx

    @staticmethod
    def _write_audit(user_id, action, details):
        log = AuditLog(
            user_id = user_id,
            action  = action,
            details = details
        )
        db.session.add(log)
  
    @staticmethod
    def receive_stock(data, performed_by):
        item = Item.query.get_or_404(data["item_id"])

        item.quantity  += data["quantity"]
        item.available += data["quantity"]

        InventoryService._record_transaction(
            item_id          = item.id,
            transaction_type = "RECEIVE",
            quantity         = data["quantity"],
            performed_by     = performed_by,
            remarks          = data.get("remarks")
        )

        InventoryService._write_audit(
            user_id = performed_by,
            action  = "RECEIVE_STOCK",
            details = f"Received {data['quantity']} units of item {item.id} ({item.name})"
        )

        db.session.commit()
        return item
   
    @staticmethod
    def dispatch_stock(data, performed_by):
        item = Item.query.get_or_404(data["item_id"])

        if item.available < data["quantity"]:
            raise ValueError(
                f"Insufficient stock. Available: {item.available}, Requested: {data['quantity']}"
            )

        item.available -= data["quantity"]

        InventoryService._record_transaction(
            item_id          = item.id,
            transaction_type = "DISPATCH",
            quantity         = data["quantity"],
            performed_by     = performed_by,
            reference_number = data.get("job_card"),
            remarks          = data.get("remarks")
        )

        InventoryService._write_audit(
            user_id = performed_by,
            action  = "DISPATCH_STOCK",
            details = f"Dispatched {data['quantity']} units of item {item.id} ({item.name}) for {data.get('job_card')}"
        )

        db.session.commit()
        return item

    @staticmethod
    def return_stock(data, performed_by):
        item = Item.query.get_or_404(data["item_id"])

        item.available += data["quantity"]

        InventoryService._record_transaction(
            item_id          = item.id,
            transaction_type = "RETURN",
            quantity         = data["quantity"],
            performed_by     = performed_by,
            reference_number = data.get("job_card"),
            remarks          = data.get("remarks")
        )

        InventoryService._write_audit(
            user_id = performed_by,
            action  = "RETURN_STOCK",
            details = f"Returned {data['quantity']} units of item {item.id} ({item.name})"
        )

        db.session.commit()
        return item
  
    @staticmethod
    def report_damage(data, performed_by):
        from models.damage_log import DamageLog

        item = Item.query.get_or_404(data["item_id"])

        if item.available < data["quantity"]:
            raise ValueError(
                f"Cannot damage more than available stock. Available: {item.available}"
            )

        item.available -= data["quantity"]
        item.quantity  -= data["quantity"]

        damage = DamageLog(
            item_id      = item.id,
            quantity     = data["quantity"],
            reason       = data.get("reason"),
            reported_by  = performed_by
        )
        db.session.add(damage)

        InventoryService._record_transaction(
            item_id          = item.id,
            transaction_type = "DAMAGE",
            quantity         = data["quantity"],
            performed_by     = performed_by,
            remarks          = data.get("reason")
        )

        InventoryService._write_audit(
            user_id = performed_by,
            action  = "REPORT_DAMAGE",
            details = f"Reported {data['quantity']} damaged units of item {item.id} ({item.name}). Reason: {data.get('reason')}"
        )

        db.session.commit()
        return item