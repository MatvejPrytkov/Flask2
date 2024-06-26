from flask import abort, jsonify, request

from api import app, db, multi_auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel  # noqa: F401
from api.schemas.author import author_schema, authors_schema


@app.route("/authors")
@multi_auth.login_required
def handle_authors():
        authors = AuthorModel.query.all()
        return authors_schema.dump(authors), 200

@app.post("/authors")
@multi_auth.login_required(role='admin')    
def handle_authors_post():
        author_data = author_schema.load(request.json)  # get_json(): json -> dict
        # author_data = author_schema.loads(request.data) # get_data: binary str -> dict

        author = AuthorModel(**author_data)
        db.session.add(author)
        try:
            db.session.commit()
            return jsonify(author_schema.dump(author)), 201
        except Exception:
            abort(400, "UNIQUE constraint failed")


@app.get("/authors/<int:author_id>")
def get_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author:
        return jsonify(author_schema.dump(author)), 200
    abort(404, f"Author with id = {author_id} not found")


@app.put("/authors/<int:author_id>")
@multi_auth.login_required
def edit_author(author_id):
    new_data = request.json
    author = AuthorModel.query.get(author_id)
    if not author:
        abort(404, f"Author with id = {author_id} not found")

    # Универсальный случай
    for key, value in new_data.items():
        setattr(author, key, value)
    try:
        db.session.commit()
        return jsonify(author_schema.dump(author)), 200
    except Exception:
        abort(400, "Database commit operation failed.")


@app.delete("/authors/<int:author_id>")
@multi_auth.login_required
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if not author:
        abort(404, f"Author with id = {author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify(message=f"Author with id={author_id} deleted successfully"), 200
    except Exception:
        abort(400, "Database commit operation failed.")
