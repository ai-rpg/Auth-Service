import json
from couchbase.options import QueryOptions
from interface.i_auth_repository import IAuthRepository
from interface.i_couchbase_repository import ICouchbaseRepository
from domain.user_model import UserModel


class AuthRepository(IAuthRepository):
    def __init__(self, i_couchbase_repository: ICouchbaseRepository()):
        self.couchbase_repository = i_couchbase_repository

    def get_user_by_username(self, username):
        scope = self.couchbase_repository.cb.scope("_default")
        sql_query = "SELECT * FROM users WHERE username = $1"
        row_iter = scope.query(
            sql_query, QueryOptions(positional_parameters=[username])
        )

        for row in row_iter:
            result: UserModel = UserModel(row["users"]["username"])
            result.disabled = row["users"]["disabled"]
            result.email = row["users"]["email"]
            result.full_name = row["users"]["full_name"]
            result.password = row["users"]["password"]
            return result

        # fake_users_db = {
        #     "johndoe": {
        #         "username": "johndoe",
        #         "full_name": "John Doe",
        #         "email": "johndoe@example.com",
        #         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        #         "disabled": "false",
        #     }
        # }
        # return fake_users_db

    def create_user(self, new_user):
        try:
            self.couchbase_repository.cb_coll.upsert(
                new_user.username, new_user.__dict__
            )
        except Exception as e:
            print(e)
