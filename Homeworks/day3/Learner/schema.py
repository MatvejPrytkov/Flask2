from marshmallow import Schema, fields
from model import Learner


class LearnerSchema(Schema):
    uid = fields.Integer()
    name = fields.String()
    final_test = fields.Boolean()

    def validate_final_test(self, value):
        if not isinstance(value, bool):
            raise ValueError("Поле 'final_test' должно быть типа 'bool'")
        return value


learner = Learner(name='Vlad', uid=10, final_test=True)
schema = LearnerSchema()
result = schema.dump(learner)
print(result)