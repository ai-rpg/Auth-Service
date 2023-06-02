from interface.i_auth_repository import IAuthRepository
from interface.i_couchbase_repository import ICouchbaseRepository
class AuthRepository(IAuthRepository):

    def __init__(self, mangement_api_token, couchbase_repository):
        self.mangement_api_token = mangement_api_token
        self.couchbase_repository = couchbase_repository

    def get_user_by_email(self, email):
        pass

    def create_user(self, email, password):
        pass
