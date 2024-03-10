from api import db


class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Author({self.name})'
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name
    #     }