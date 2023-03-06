from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("students", __name__, description='Operations on students')

@blp.route("/student")
class StudentList(MethodView):
    def get(self):
        """
        Get all students
        """
        pass


@blp.route('/student/<int:student_id>')
class Student(MethodView):
    def get(self, student_id):
        """
        Get a student by id
        """
        pass

    def patch(self, student_id):
        """
        Update student enrollment status
        """
        pass

    def delete(self, student_id):
        """
        Delete a student
        """
        pass


@blp.route('/student/<int:student_id>/cgpa')
class StudentCGPA(MethodView):
    def get(self, student_id):
        """
        Get student cgpa
        """
        pass
