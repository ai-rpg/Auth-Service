import abc 

class IAuthRepository(metaclass=abc.ABCMeta):
    
    @abc.abstractclassmethod
    def get_user_by_email(self, email):
        raise NotImplementedError

    @abc.abstractclassmethod
    def create_user(self, email, password):
        raise NotImplementedError
         