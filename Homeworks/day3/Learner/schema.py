"""
https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation

=== Warning ===
Validation occurs on deserialization but not on serialization. 
To improve serialization performance, data passed to Schema.dump() are considered valid.
"""

from marshmallow import Schema, fields, validates, ValidationError
from model import Learner


def check(value: str):
    if len(value) < 3:
        raise ValidationError(f"{value} too short for field.")
    return value


class LearnerSchema(Schema):
    uid = fields.Integer(required=True)
    name = fields.String(validate=check)  # Внешняя функция в роли валидатора
    final_test = fields.Boolean()

    @validates("uid")
    def check_uid(self, n):
        """Пример метода-валидатора для конкретного поля"""
        if n < 1:
            raise ValidationError(f"{n} must be positive")

    @validates("final_test")
    def validate_final_test(self, value):
        if not value:
            raise ValidationError("Поле 'final_test' должно быть 'truthy'")
        return value


learner = Learner(name="Vlad", uid=10, final_test=True)
print(learner)
schema = LearnerSchema()
result = schema.dumps(learner)
print(result, type(result))
de_learner = schema.loads(result)
print(f"{de_learner = }")
