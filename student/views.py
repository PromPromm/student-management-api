from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from flask_jwt_extended import jwt_required
from models.user import User
from schemas import UserSchema, StudentChangePasswordSchema
from utils import db
from werkzeug.security import check_password_hash, generate_password_hash

blp = Blueprint("students", __name__, description='Operations on students')

@blp.route("/student")
class StudentList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all students
        """
        students = User.query.filter(User.is_admin != True)
        return students


@blp.route('/student/<int:student_id>')
class Student(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, student_id):
        """
        Get a student by id
        """
        student = User.get_by_id(student_id)
        return student


    def patch(self, student_id):
        """
        Update student enrollment status
        """
        pass

    @jwt_required()
    def delete(self, student_id):
        """
        Delete a student by id
        """
        student = User.get_by_id(student_id)

        db.session.delete(student)
        db.session.commit()

        return {"message": "Student deleted"}


@blp.route('/student/change_password')
class StudentChangePassword(MethodView):
    @blp.arguments(StudentChangePasswordSchema)
    @blp.response(200, UserSchema)
    def patch(self, user_data):
        """
        Endpoint for student to change the automatically generated password
        """
        user = User.query.filter_by(student_id=user_data["student_id"]).first()

        if user and check_password_hash(user.password, user_data["password"]):
            if user_data["new_password"] == user_data["confirm_new_password"]:
                user.password = generate_password_hash(user_data["new_password"])
                user.enrollment_status = 'ACTIVE'
                db.session.commit()
                return user
            abort(401, "New password and confirm password do not match")
        abort(401, 'Invalid credentials')


@blp.route('/student/<int:student_id>/cgpa')
class StudentCGPA(MethodView):
    def get(self, student_id):
        """
        Get student cgpa
        """
        pass
