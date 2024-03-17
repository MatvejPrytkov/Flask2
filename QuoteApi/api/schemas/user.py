from flask import request
from marshmallow import post_load, validate, fields
from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ("password_hash",)

    username = ma.auto_field(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=15))

    @post_load
    def make_user(self, data: dict, **kwargs):
        if request.method == "POST":
            return UserModel(**data)
        return data


user_schema = UserSchema()