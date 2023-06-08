import abc
from domain.create_user_model import CreateUserModel
class IAuthRepository(metaclass=abc.ABCMeta):
    
    @abc.abstractclassmethod
    def get_user_by_username(self, email):
        raise NotImplementedError

    @abc.abstractclassmethod
    def create_user(self, new_user: CreateUserModel):
        raise NotImplementedError
         