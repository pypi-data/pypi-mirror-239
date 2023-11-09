from typing import Tuple
class Config:
    EXCLUDE_START = ['__', "_Config__", "EXCLUDE_START", "keys"]
    """
    Configure for function.
    Not save the key start_with '__'
    """
    def __init__(self, *a, **kwargs):
        self.__args = list(a)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __iter__(self):
        return iter(self.__args)

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        _ = []
        for k in dir(self):
            _flag = True
            for not_start in Config.EXCLUDE_START:
                if k.startswith(not_start):
                    _flag = False
                    break
            if _flag:
                _ += [k]
        return _

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__args) + ", " + str({k: getattr(self, k) for k in self.keys()})