from api import db


class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    surname = db.Column(db.String(32), server_default="Petrov", default="Ivanov", nullable=False)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name, surname='Ivanov'):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'Author({self.name})'
