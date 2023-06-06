from interface.i_auth_repository import IAuthRepository
from interface.i_couchbase_repository import ICouchbaseRepository
class AuthRepository(IAuthRepository):

    def __init__(self, couchbase_repository):
        self.couchbase_repository = couchbase_repository

    def get_user_by_username(self, username):
        fake_users_db = {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "disabled": False,
            }
        }
        return fake_users_db
        
    def create_user(self, email, password):
        pass
