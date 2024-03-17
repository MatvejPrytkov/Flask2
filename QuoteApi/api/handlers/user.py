from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema
from flask import abort, request, jsonify


# url: /users/<int:user_id>
@app.get("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = UserModel.query.get_or_404(user_id, f'User with id={user_id} not found')
    return user_schema.dump(user), 200


# url: /users
@app.get("/users")
def get_users():
    users = UserModel.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200


# url: /users
@app.post("/users")
def create_user():
    if request.method == "POST":
        try:
            user = user_schema.load(request.json)
        except ValidationError as error:
            return jsonify(error.messages)

    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201
    except Exception:
        abort(400, "unique contraint failed.")


@app.put("/users/<int:user_id>")
def change_user(user_id):
    user = UserModel.query.get_or_404(user_id, f"User with id = {user_id} not found")

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as error:
        return jsonify(error.messages)
    
    for key, value in user_data.items():
        setattr(user, key, value)
    try:
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception:
        abort(400, "Database commit operation failed.")


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    user = UserModel.query.get_or_404(user_id, f"User with id = {user_id} not found")
    db.session.delete(user)
    try:
        db.session.commit()
        return jsonify(message=f"User with id={user_id} deleted successfully"), 200
    except Exception:
        abort(400, "Database commit operation failed.")