from marshmallow import Schema, fields


class InventoryTransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    transaction_type = fields.Str(required=True)
    quantity = fields.Int(required=True)
    reference = fields.Str()
    remarks = fields.Str()
    item_id = fields.Int(required=True)
    performed_by = fields.Int()

    created_at = fields.DateTime(dump_only=True)