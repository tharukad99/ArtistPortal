# from functools import wraps
# from flask import abort
# from flask_login import current_user

# def admin_required(view_func):
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#         if not current_user.is_authenticated:
#             abort(403)
#         if not current_user.is_admin():
#             abort(403)
#         return view_func(*args, **kwargs)
#     return wrapper
# artistportal/routes/decorators.py
from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        # Your User model should have IsAdmin boolean
        if not getattr(current_user, "IsAdmin", False):
            abort(403)
        return view_func(*args, **kwargs)
    return wrapper
