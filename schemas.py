from marshmallow import Schema, fields
from models.user import EnrollmentStatus

class PlainCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    teacher = fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)

class StudentLoginSchema(Schema):
    student_id = fields.Str(required=True)
    password = fields.Str(required=True)

class AdminLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class StudentChangePasswordSchema(StudentLoginSchema):
    new_password = fields.Str(required=True)
    confirm_new_password = fields.Str(required=True)

class AdminChangePasswordSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_new_password = fields.Str(required=True)

class UserSchema(PlainUserSchema):
    student_id = fields.Str(dump_only=True)
    password = fields.Str(required=True)
    enrollment_status = fields.Enum(EnrollmentStatus, by_value=True)
    is_admin = fields.Boolean()
    date_created = fields.DateTime()
    courses = fields.Nested(PlainCourseSchema())

    