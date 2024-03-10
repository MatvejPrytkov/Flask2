from api import app, db
from flask import request, abort, jsonify
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from api.schemas.quote import quote_schema, quotes_schema, quote_rating_schema
from marshmallow import ValidationError


# GET на url: /authors/<int:id>/quotes      # получить все цитаты автора с quote_id = <int:quote_id>
@app.get("/authors/<int:author_id>/quotes")
def get_quote_by_author(author_id):
    quotes_lst = db.session.query(QuoteModel).filter_by(author_id=author_id)
    return jsonify(quotes_schema.dump(quotes_lst)), 200


@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote_to_author(author_id):
    """function to create new quote to author"""
    author = AuthorModel.query.get_or_404(author_id)
    try:
        data = quote_rating_schema.loads(request.data)
    except ValidationError:
        data = quote_schema.loads(request.data)
        data["rating"] = 1

    # После валидации создаем новую цитату
    new_quote = QuoteModel(author, **data)
    db.session.add(new_quote)
    try:
        db.session.commit()
        out_data = quote_rating_schema.dump(new_quote)
        print(f'{out_data = }')
        return quote_rating_schema.dump(new_quote), 201
    except Exception:
        abort(400, "Database commit operation failed.")


@app.route("/quotes")
def get_quotes():
    """Сериализация: list[quotes] -> list[dict] -> str(JSON)"""
    quotes_db = QuoteModel.query.all()
    return jsonify(quote_rating_schema.dump(quotes_db, many=True)), 200


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return jsonify(quote_rating_schema.dump(quote)), 200
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
    quote = QuoteModel.query.get_or_404(quote_id, f"Quote id = {quote_id} not found")

    try:
        data = quote_rating_schema.loads(request.data)
    except ValidationError:
        data = quote_schema.loads(request.data)

    # Универсальный случай
    for key, value in data.items():
        setattr(quote, key, value)

    try:
        db.session.commit()
        return jsonify(quote_rating_schema.dump(quote)), 200
    except Exception:
        abort(500)


@app.route("/quotes/filter")
def get_quotes_by_filter():
    kwargs = request.args

    # Универсальное решение
    quotes_db = QuoteModel.query.filter_by(**kwargs).all()

    if quotes_db:
        return jsonify(quotes_schema.dump(quotes_db)), 200
    return jsonify([]), 200
