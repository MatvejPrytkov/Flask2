from my_app.hello.models import MESSAGES
from flask import Blueprint

hello = Blueprint('hello', __name__)



@hello.route("/")
@hello.route("/hello")
def hello_world():
    return MESSAGES["default"]


@hello.route("/show/<key>")
def get_message(key):
    return MESSAGES.get(key) or f'{key} not found!'