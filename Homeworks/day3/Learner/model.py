from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Learner(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    final_test = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Learner({self.name}, {self.final_test})'