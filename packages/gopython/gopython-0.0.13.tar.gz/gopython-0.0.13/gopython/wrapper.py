from functools import wraps
from .api.auth import AuthAPI
from flask import Flask, request, abort, session, render_template

class ACL(AuthAPI):
    def __init__(self, app=None):
        super().__init__()
        self.app = app


    def acl_auth(self, role, permission):
        def decorator(view_func):
            @wraps(view_func)
            def decorated_view(*args, **kwargs):
                user_id = str(session.get('user_id'))  # Extract user_id from query parameters
                print("user_id:",user_id)
                if not user_id:
                    abort(403)  # If user_id is not provided in the query parameters, deny access

                if self._is_authorized(role, permission, user_id):
                    return view_func(*args, **kwargs)
                else:
                    abort(403)  # You can return a custom error page or message if access is denied

            return decorated_view
        return decorator