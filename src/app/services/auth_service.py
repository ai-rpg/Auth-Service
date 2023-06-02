from interface.i_auth_service import IAuthService

class AuthService(IAuthService):
    def __init__(self, auth_repository):
        self.auth_repository = auth_repository

    def register_user(self, email, password):
        # Implement the logic to register a user
        user = self.auth_repository.get_user_by_email(email)
        if user is not None:
            return 'User already exists'
        self.auth_repository.create_user(email, password)
        return 'User registered successfully'

    def authenticate_user(self, email, password):
        # Implement the logic to authenticate a user
        user = self.auth_repository.get_user_by_email(email)
        if user is None:
            return 'User not found'
        # Perform authentication logic (e.g., verify password)
        return 'User authenticated successfully'