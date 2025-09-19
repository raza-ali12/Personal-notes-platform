from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=1, max=120))
    created_at = fields.DateTime(dump_only=True)

class UserRegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=1, max=120))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(allow_none=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class NoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    content = fields.Str(allow_none=True)

# Initialize schemas
user_schema = UserSchema()
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
note_update_schema = NoteUpdateSchema()
