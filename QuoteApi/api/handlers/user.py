from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


# url: /users/<int:user_id>
def get_user_by_id(user_id):
    ...

# url: /users
def get_users(user_id):
    ...

# url: /users
def create_user():
    ...