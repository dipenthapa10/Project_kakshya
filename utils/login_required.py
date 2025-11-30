from functools import wraps
from flask import session, redirect

def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):

            if "user_id" not in session:
                return redirect("/auth/login")

            if role and session.get("role") != role:
                return redirect("/auth/login")

            return fn(*args, **kwargs)
        return decorated
    return wrapper
