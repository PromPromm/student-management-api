from .db import db
from datetime import date
import random

def generate_student_id():
    student_info = ['STA', str(date.today().year), str(random.randint(1000,9999))]
    student_id = "/".join(student_info)
    return student_id
