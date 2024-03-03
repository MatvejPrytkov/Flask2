from api import app, db
from flask import request, abort, jsonify
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from . import validate



# GET на url: /authors/<int:id>/quotes      # получить все цитаты автора с quote_id = <int:quote_id>
@app.get("/authors/<int:author_id>/quotes")
def get_quote_by_author(author_id):
    quotes_lst = db.session.query(QuoteModel).filter_by(author_id=author_id)   
    quotes_lst_dct = []
    for quote in quotes_lst:
        quotes_lst_dct.append(quote.to_dict())
    return jsonify(quotes_lst_dct), 200


@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote_to_author(author_id):
    """ function to create new quote to author"""
    author = AuthorModel.query.get(author_id)
    data = request.json
    # Валидация данных
    data = validate(data)

    # После валидации создаем новую цитату
    new_quote = QuoteModel(author, **data)
    db.session.add(new_quote)
    try:
        db.session.commit()
        return new_quote.to_dict(), 201
    except Exception:
        abort(400, "Database commit operation failed.")


@app.route("/quotes")
def get_quotes():
    """ Сериализация: list[quotes] -> list[dict] -> str(JSON) """
    quotes_db = QuoteModel.query.all()
    quotes = []
    for quote_db in quotes_db:
        quotes.append(quote_db.to_dict())
    
    return jsonify(quotes), 200


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return jsonify(quote.to_dict()), 200
    abort(404, f"Quote with id={quote_id} not found")


@app.delete("/quotes/<int:quote_id>")
def delete(quote_id):
    quote = db.session.get(QuoteModel, quote_id)
    if quote is not None:
        db.session.delete(quote)
        db.session.commit()
        return jsonify(message=f"Quote with id={quote_id} deleted."), 200
    abort(404, f"Quote id = {quote_id} not found")


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id):
    data = request.json
    quote = QuoteModel.query.get(quote_id)
    if not quote:
        abort(404, f"Quote id = {quote_id} not found")

    # Валидация данных
    data = validate(data, "put")
        
    # Универсальный случай
    for key, value in data.items():
        setattr(quote, key, value)

    try:
        db.session.commit()
        return jsonify(quote.to_dict()), 200
    except Exception:
        abort(500)


@app.route("/quotes/filter")
def get_quotes_by_filter():
    kwargs = request.args

    # Универсальное решение  
    quotes_db = QuoteModel.query.filter_by(**kwargs).all()

    if quotes_db:
        quotes = []
        for quote in quotes_db:
            quotes.append(quote.to_dict())      
        return jsonify(quotes), 200
    return jsonify([]), 200
