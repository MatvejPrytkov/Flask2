from passlib.apps import custom_app_context as pwd_context
from api import app, db, Config
# from itsdangerous import URLSafeSerializer
# from itsdangerous import BadSignature
import jwt
from time import time


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def __repr__(self):
        return f'User({self.username})'
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def generate_auth_token(self):
    #    s = URLSafeSerializer(Config.SECRET_KEY)
    #    return s.dumps({'id': self.id})
        token = jwt.encode({"id": self.id, "exp": int(time() + 3600)},
                           Config.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_auth_token(token):
        # s = URLSafeSerializer(app.config["SECRET_KEY"])
        # try:
        #     data = s.loads(token)
        # except BadSignature:
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except Exception:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user