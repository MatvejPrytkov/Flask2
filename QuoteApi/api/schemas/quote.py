from marshmallow import ValidationError, fields, EXCLUDE, validate
from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


def rating_validate(value: int):
    return value in range(1, 6) # if False -> raise ValidationError



class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field()
    author = ma.Nested(AuthorSchema())
    rating = fields.Integer(strict=True, validate=rating_validate)


quote_schema = QuoteSchema(exclude=["rating"])
quote_rating_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)
