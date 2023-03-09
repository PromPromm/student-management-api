from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from models.courses import Course
from schemas import PlainCourseSchema
from flask import abort

blp = Blueprint("courses", __name__, description='Operations on courses')


@blp.route("/course")
class CourseList(MethodView):
    @jwt_required()
    @blp.response(200, PlainCourseSchema(many=True))
    def get(self):
        """
        Get all courses
        """
        courses = Course.query.all()
        return courses
    

    @jwt_required()
    @blp.arguments(PlainCourseSchema)
    @blp.response(201, PlainCourseSchema)
    def post(self, course_data):
        """
        Create a course
        """
        course = Course.query.filter_by(name=course_data['name']).first()
        if course:
            abort(401, "Course with that name exists")
        new_course = Course(name=course_data["name"], teacher=course_data["teacher"])
        new_course.save()
        return new_course

@blp.route("/course/<int:course_id>")
class CoursebyId(MethodView):
    @blp.response(200, PlainCourseSchema)
    @jwt_required()
    def get(self, course_id):
        """
        Get course by id
        """
        course = Course.get_by_id(course_id)
        return course


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
