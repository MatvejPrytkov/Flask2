from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
basic_auth = HTTPBasicAuth() 
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user_ba = UserModel.query.filter_by(username = username).one_or_none()
    if not user_ba or not user_ba.verify_password(password):
        return False
    g.user = user_ba
    return user_ba


@token_auth.verify_token
def verify_token(token_in):
   from api.models.user import UserModel
   user_ta = UserModel.verify_auth_token(token_in)
   print(f"{user_ta=}")
   return user_ta


from config import Config        # noqa: E402, F401
from api.handlers import author  # noqa: E402, F401
from api.handlers import quote   # noqa: E402, F401
from api.handlers import user    # noqa: E402, F401
from api.handlers import token   # noqa: E402, F401