from api import app
from flask import jsonify
from werkzeug.exceptions import HTTPException



def validate(in_data: dict, method="post") -> dict:
    rating = in_data.setdefault("rating", 1)
    if rating not in range(1, 6) and method == "post":
        in_data["rating"] = 1
    elif rating not in range(1, 6) and method == "put":
        in_data.pop("rating")
    in_data.setdefault("text", "text")
    return in_data


# Обработка ошибок и возврат сообщения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code