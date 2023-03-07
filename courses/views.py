from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("courses", __name__, description='Operations on courses')


@blp.route("/course")
class CourseList(MethodView):
    def get(self):
        """
        Get all courses
        """
        pass

    def post(self):
        """
        Create a course
        """
        pass

@blp.route("/course/<int:course_id>")
class Course(MethodView):
    def get(self, course_id):
        """
        Get course by id
        """
        pass

    def delete(self, course_id):
        """
        Delete a course by id
        """
        pass


@blp.route("/course/<int:course_id>/enroll")
class CourseEnroll(MethodView):
    def post(self):
        """
        Enrolling for a course
        """
        pass


@blp.route("/student/<int:student_id>/courses/")
class StudentCourseList(MethodView):
    def get(self, student_id):
        """
        Get all courses a student offers
        """
        pass

    def patch(self, student_id):
        """
        Unenroll a student from a course
        """
        pass


@blp.route("/course/<int:course_id>/students")
class CourseStudentsList(MethodView):
    def get(self, course_id):
        """
        Get all students that take a course
        """
        pass

@blp.route("/course/<int:course_id>/score-upload")
class ScoreUpload(MethodView):
    def post(self, course_id):
        """
        Upload course results
        """
        pass
