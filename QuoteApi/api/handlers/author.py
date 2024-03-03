from api import app, db
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.author import author_schema, authors_schema




@app.route("/authors", methods=["GET", "POST"])
def handle_authors():
    if request.method == "GET":
        authors = AuthorModel.query.all()
        return authors_schema.dump(authors), 200
      
    if request.method == "POST":
        author_data = request.json
        author = AuthorModel(author_data.get("name", "Ivan"))
        db.session.add(author)
        try:
            db.session.commit()
            return jsonify(author.to_dict()), 201
        except Exception:       
            abort(400, "UNIQUE constraint failed")


@app.get("/authors/<int:author_id>")
def get_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author:
        return jsonify(author.to_dict()), 200
    abort(404, f"Author with id = {author_id} not found")


@app.put("/authors/<int:author_id>")
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
        return jsonify(author.to_dict()), 200
    except Exception:
        abort(400, "Database commit operation failed.")


@app.delete("/authors/<int:author_id>")
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