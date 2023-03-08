from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from models.user import User
from schemas import UserSchema
from utils import db

blp = Blueprint("students", __name__, description='Operations on students')

@blp.route("/student")
class StudentList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all students
        """
        students = User.query.filter(User.student_id != "null")
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


@blp.route('/student/<int:student_id>/cgpa')
class StudentCGPA(MethodView):
    def get(self, student_id):
        """
        Get student cgpa
        """
        pass
