from api.models.author import AuthorModel
from api import db


class QuoteModel(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id), nullable=False)
    text = db.Column(db.String(255), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False, default="1", server_default="3")

    def __init__(self, author, text, rating):
        self.author_id = author.id
        self.text  = text
        self.rating = rating

    def __repr__(self):
        return f'Quote({self.text})'
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "author": self.author_id,
    #         "text": self.text,
    #         "rating": self.rating
    #     }