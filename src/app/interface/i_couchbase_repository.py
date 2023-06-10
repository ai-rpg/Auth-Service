import abc


class ICouchbaseRepository(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def get(self):
        raise NotImplementedError
