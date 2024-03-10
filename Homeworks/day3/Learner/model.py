


class Learner(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    final_test = db.Column(db.Boolean, nullable=False)