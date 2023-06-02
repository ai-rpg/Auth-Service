import abc

class IAuthService(metaclass=abc.ABCMeta):
    
    @abc.abstractclassmethod
    def register_user(self, email, password):
        raise NotImplementedError

    @abc.abstractclassmethod
    def authenticate_user(self, email, password):
        raise NotImplementedError