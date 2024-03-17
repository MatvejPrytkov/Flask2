from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user_i = UserModel.query.filter_by(username = username).one_or_none()
    if not user_i or not user_i.verify_password(password):
        return False
    g.user = user_i
    return user_i


from api.handlers import author  # noqa: E402, F401
from api.handlers import quote  # noqa: E402, F401
from api.handlers import user  # noqa: E402, F401