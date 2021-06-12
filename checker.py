# This module provides a function decorator that checks if the user is logged in to the web application.

from flask import session
from functools import wraps

def check_logged_in(func):
# A function decorator that will check if a user is logged in.
    @wraps(func)    # <-- This must be called when creating a decorator; otherwise a function can forget its identity (this has to deal with how functions are processed by the interpreter)
    def wrapper(*args, **kwargs):   # Any arguments from the 'func' will be passed here, because we're returning 'wrapper' at the end
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return 'You are NOT logged in.'
    return wrapper