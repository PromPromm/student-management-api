from .db import db
from .mail import mail
from datetime import date
import random
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify


def generate_student_id():
    student_info = ["STA", str(date.today().year), str(random.randint(1000, 9999))]
    student_id = "/".join(student_info)
    return student_id


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(Error="Admins only!"), 403

        return decorator

    return wrapper


def super_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["super_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(Error="Super Admins only!"), 403

        return decorator

    return wrapper


def grade_to_point_converter(grade: str) -> int:
    if grade == "A":
        point = 5
    elif grade == "B":
        point = 4
    elif grade == "C":
        point = 3
    elif grade == "D":
        point = 2
    elif grade == "E":
        point = 1
    else:
        point = 0
    return point
