from config import SECRET_KEY, ALGORITHM
from interface.i_auth_service import IAuthService
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from domain.user_model import UserModel
from fastapi import Depends

class AuthService(IAuthService):
    def __init__(self, auth_repository):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.auth_repository = auth_repository

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, username: str):
        return self.auth_repository.get_user_by_username(username)

    def authenticate_user(self, username:str, password:str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user[username]['hashed_password']):
            return False
        return user
        
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    async def get_current_user(self, token:str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user: UserModel):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user