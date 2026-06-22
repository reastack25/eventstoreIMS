from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    quantity = fields.Int()
    available = fields.Int()
    status = fields.Str()