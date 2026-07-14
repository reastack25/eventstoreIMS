# schemas/auth_schema.py

from marshmallow import Schema, fields, validate
from utils.roles import Role

class RegisterSchema(Schema):
    full_name = fields.Str(required=True)
    email     = fields.Email(required=True)
    password  = fields.Str(required=True)
    role      = fields.Str(
        load_default = Role.STORE_KEEPER,
        validate     = validate.OneOf([
            Role.ADMIN,
            Role.STORE_MANAGER,
            Role.STORE_KEEPER,
            Role.FIELD_STAFF
        ])
    )

class LoginSchema(Schema):
    email    = fields.Email(required=True)
    password = fields.Str(required=True)