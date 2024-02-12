from marshmallow import Schema, fields


class ListTasksSchema(Schema):
    """List tasks schema."""

    data = fields.List(fields.Nested("TaskSchema"))


class TaskSchema(Schema):
    """Task schema."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    done = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TaskUpdateSchema(Schema):
    """Task update schema."""

    name = fields.Str()
    done = fields.Bool()


class UserSchema(Schema):
    """User schema."""

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """User login schema."""

    username = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
