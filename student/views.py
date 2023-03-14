from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from flask_jwt_extended import jwt_required
from models.user import User, EnrollmentStatus
from schemas import UserSchema, StudentChangePasswordSchema, ChangeEnrollmentStatusSchema
from utils import db
from werkzeug.security import check_password_hash, generate_password_hash
from utils import admin_required
from http import HTTPStatus

blp = Blueprint("students", __name__, description='Operations on students')

@blp.route("/student")
class StudentList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.doc(description='Get all registered students. Can be accessed by only an admin')
    @jwt_required()
    @admin_required()
    def get(self):
        """
        Get all students
        """
        students = User.query.filter(User.is_admin != True)
        return students, HTTPStatus.OK


@blp.route('/student/<int:student_id>')
class Student(MethodView):
    @blp.doc(description='Get a student by id. Can be accessed by only an admin',
             params={
                    "student_id": "The id of the student"
             }
             )
    @blp.response(200, UserSchema)
    @jwt_required()
    @admin_required()
    def get(self, student_id):
        """
        Get a student by id
        """
        student = User.get_by_id(student_id)
        return student, HTTPStatus.OK


    @blp.doc(description='Update a student enrollment by id. Can be accessed by only an admin',
             params={
                    "student_id": "The id of the student"
             }
             )
    @blp.arguments(ChangeEnrollmentStatusSchema)
    @blp.response(200, UserSchema)
    @jwt_required()
    @admin_required()
    def put(self, data, student_id):
        """
        Update student enrollment status
        """
        student = User.get_by_id(student_id)
        student.enrollment_status = data['enrollment_status']
        db.session.commit()
        return student, HTTPStatus.OK
        

    
    @blp.doc(description='Delete a student by id. Can be accessed by only an admin. Takes a fresh jwt access token',
             params={
                    "student_id": "The id of the student"
             }
             )
    @admin_required()
    @jwt_required(fresh=True)
    def delete(self, student_id):
        """
        Delete a student by id
        """
        user = User.get_by_id(student_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "Student deleted"}, HTTPStatus.OK


@blp.route('/student/change_password')
class StudentChangePassword(MethodView):
    @blp.arguments(StudentChangePasswordSchema)
    @blp.doc(description='Change student password.')
    @blp.response(200, UserSchema)
    def put(self, user_data):
        """
        Student change password route
        """
        user = User.query.filter_by(student_id=user_data["student_id"]).first()

        # checks if user exists and password matches
        if user and check_password_hash(user.password, user_data["password"]):
            # checks if user has been expelled
            if user.enrollment_status == EnrollmentStatus.EXPELLED:
                return {"Error": "You are no longer a student"}, HTTPStatus.UNAUTHORIZED
            # check if the new_password field and confirm_new_password field is the same
            if user_data["new_password"] == user_data["confirm_new_password"]:
                user.password = generate_password_hash(user_data["new_password"])
                user.enrollment_status = 'ACTIVE'
                db.session.commit()
                return user, HTTPStatus.OK
            abort(400, "New password and confirm password do not match")
        abort(403, 'Invalid credentials')


@blp.route('/student/<int:student_id>/cgpa')
class StudentCGPA(MethodView):
    def get(self, student_id):
        """
        Get student cgpa
        """
        pass
