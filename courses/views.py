from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from models.courses import Course
from models.user import User
from models.scores import Score
from utils import db
from schemas import PlainCourseSchema, UserSchema, ScoreUploadSchema
from flask import abort, jsonify

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


@blp.route("/course/<int:course_id>/enroll/<int:student_id>")
class CourseEnroll(MethodView):
    @jwt_required()
    @blp.response(201, UserSchema)
    def post(self, course_id, student_id):
        """
        Enrolling for a course
        """
        course = Course.get_by_id(course_id)
        student = User.get_by_id(student_id)
        student.courses.append(course)

        db.session.commit()
        return student
    

@blp.route("/course/<int:course_id>/unenroll/<int:student_id>")
class CourseUnEnroll(MethodView):
    @blp.response(201, UserSchema)
    @jwt_required()
    def patch(self, student_id, course_id):
        """
        Unenroll a student from a course
        """
        course = Course.get_by_id(course_id)
        student = User.get_by_id(student_id)
        student.courses.remove(course)
        
        db.session.commit()
        return student


@blp.route("/courses/<int:student_id>")
class StudentCourseList(MethodView):
    @jwt_required()
    def get(self, student_id):
        """
        Get all courses a student offers
        """
        course_list = []
        student = User.get_by_id(student_id)
        for course in student.courses:
            course_list.append(course.name)
        return jsonify(course_list)
    


@blp.route("/course/<int:course_id>/students")
class CourseStudentsList(MethodView):
    @jwt_required()
    def get(self, course_id):
        """
        Get all students that take a course
        """
        student_id_list = []
        course = Course.get_by_id(course_id)
        for student in course.users:
            student_id_list.append(student.student_id)
        return jsonify(student_id_list)
        

@blp.route("/course/<int:course_id>/score-upload")
class ScoreUpload(MethodView):
    @blp.arguments(ScoreUploadSchema)
    def post(self, result_data, course_id):
        """
        Upload course results
        """
        data = list(result_data.values())
        course = Course.get_by_id(course_id)
        for student_id, score in data[0].items():
            student = User.query.filter_by(student_id=student_id).first()
            print(student.courses)
            if course in student.courses:
                existing_score = Score.query.filter_by(user_id=student.id, course_id=course_id).first()
                if existing_score:
                    abort(500, "Score already exists for this course")
                score = Score(score=score, course_id=course_id, user_id=student.id)
                db.session.add(score)
                db.session.commit()
                return {"message": "Result uploaded"}
            return {"message": "Student isn't registered for this course"}
