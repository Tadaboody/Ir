import os, pickle
from functools import wraps
import builtins
from typing import Callable


class memorize:
    def __init__(self, protocol=pickle,timeout=None):
        self.protocol=protocol
        self.timeout = timeout

    def invalidate(self):
        os.remove(self.PICKLE_NAME)
    def __call__(self,fun,*args,**kwargs):
        self.PICKLE_NAME = fun.__name__ + '_pickle.' + self.protocol.__name__
        @wraps(fun)
        def wrapped_fun(*args,**kwargs):
            try:
                with open(self.PICKLE_NAME, 'rb') as pickle_file:
                    return self.protocol.load(pickle_file)
            except FileNotFoundError:
                result = fun(*args,**kwargs)
                with open(self.PICKLE_NAME,'wb') as pickle_file:
                    self.protocol.dump(result, pickle_file)
                return result
        return wrapped_fun
