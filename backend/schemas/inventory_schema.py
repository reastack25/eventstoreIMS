from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    quantity = fields.Int()
    available = fields.Int()
    status = fields.Str()
    category_id = fields.Int(required=True)