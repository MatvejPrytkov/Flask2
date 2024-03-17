from marshmallow import validate, fields
from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel


    username = ma.auto_field(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=15))


user_schema = UserSchema()