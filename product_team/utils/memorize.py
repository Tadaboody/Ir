import os, pickle
from functools import wraps
import builtins
from typing import Callable
from os.path import join
from product_team import SAVE_DIR
from product_team.utils import s_dump, s_load

def memorize(fun):
    PICKLE_NAME = fun.__name__ +  '.p'
    PICKLE_NAME = join(SAVE_DIR,PICKLE_NAME)
    @wraps(fun)
    def wrapped_fun(*args,**kwargs):
        try:
            with open(PICKLE_NAME, 'rb') as pickle_file:
                return pickle.load(pickle_file)
        except FileNotFoundError:
            result = fun(*args,**kwargs)
            try:
                with open(PICKLE_NAME,'wb') as pickle_file:
                    pickle.dump(result, pickle_file)
            except MemoryError:
                print("Memory Error,could not save pickle")
                os.remove(PICKLE_NAME)
            return result
    return wrapped_fun

def stream_memorize(fun):
    PICKLE_NAME = fun.__name__ +  '.p'
    PICKLE_NAME = join(SAVE_DIR,PICKLE_NAME)
    @wraps(fun)
    def wrapped_fun(*args,**kwargs):
        try:
            with open(PICKLE_NAME, 'rb') as pickle_file:
                a =  s_load(pickle_file)
                return a
        except FileNotFoundError:
            result = fun(*args,**kwargs)
            try:
                with open(PICKLE_NAME,'wb') as pickle_file:
                    s_dump(result, pickle_file)
            except MemoryError:
                print("Memory Error,could not save pickle")
                os.remove(PICKLE_NAME)
            return result
    return wrapped_fun
