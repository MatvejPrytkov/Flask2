from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


from api.handlers import author  # noqa: E402, F401
from api.handlers import quote  # noqa: E402, F401
from api.handlers import user  # noqa: E402, F401