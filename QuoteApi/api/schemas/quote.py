from marshmallow import ValidationError, fields, EXCLUDE, validate
from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


def rating_validate(value: int):
    if value > 5:
        ValidationError("Rating field out of range.")



class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field()
    author = ma.Nested(AuthorSchema())


class QuoteRatingSchema(QuoteSchema):
    rating = fields.Integer(strict=True, validate=validate.Range(min=1, max=5))


quote_schema = QuoteSchema()
quote_rating_schema = QuoteRatingSchema()
quotes_schema = QuoteSchema(many=True)
