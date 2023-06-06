import abc
from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from domain.user_model import UserModel

class IAuthService(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def verify_password(self, plain_password, hashed_password):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_password_hash(self, password):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_user(self, db, username: str):
        raise NotImplementedError

    @abc.abstractclassmethod
    def authenticate_user(self, db, username:str, password:str):
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        raise NotImplementedError

    @abc.abstractclassmethod
    async def get_current_user(self, token: str):
        raise NotImplementedError

    @abc.abstractclassmethod
    async def get_current_active_user(
        self, current_user: UserModel
    ):
        raise NotImplementedError