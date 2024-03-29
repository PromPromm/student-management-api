from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.courses import Course
from models.user import User, EnrollmentStatus
from models.scores import Score
from utils import db
from schemas import PlainCourseSchema, UserSchema, ScoreUploadSchema
from flask import jsonify
from utils import admin_required
from http import HTTPStatus

blp = Blueprint("courses", __name__, description='Operations on courses')


@blp.route("/course")
class CourseList(MethodView):
    @jwt_required()
    @admin_required()
    @blp.response(200, PlainCourseSchema(many=True))
    @blp.doc(description="Get all courses. Can be accessed by only admins")
    def get(self):
        """
        Get all courses
        """
        courses = Course.query.all()
        return courses, HTTPStatus.OK
    

    @jwt_required()
    @admin_required()
    @blp.doc(description="Create a course. Can be accessed by only admins")
    @blp.arguments(PlainCourseSchema)
    def post(self, course_data):
        """
        Create a course
        """
        course = Course.query.filter_by(name=course_data['name']).first()
        # checks if course with that name exists
        if course:
            return {"Error": "Course with that name exists"}, HTTPStatus.BAD_REQUEST
        new_course = Course(name=course_data["name"], teacher=course_data["teacher"], unit=course_data['unit'])
        new_course.save()
        return {"Name": new_course.name, "Teacher": new_course.teacher, "Unit": new_course.unit}, HTTPStatus.CREATED


@blp.route("/course/<int:course_id>")
class CoursebyId(MethodView):
    @blp.response(200, PlainCourseSchema)
    @jwt_required()
    @admin_required()
    @blp.doc(description="Retrieve a course by id. Can be accessed by only admins",
             params={
                "course_id": "The course id"
             }
             )
    def get(self, course_id):
        """
        Get course by id
        """
        course = Course.get_by_id(course_id)
        return course, HTTPStatus.OK


@blp.route("/course/<int:course_id>/enroll/<int:student_id>")
class CourseEnroll(MethodView):
    @jwt_required()
    @admin_required()
    @blp.response(200, UserSchema)
    @blp.doc(description='Enroll a student in a course. Can be accessed by only admins',
             params={
                "course_id": "The id of the course to enroll for",
                "student_id": "The id of the student to enroll"
             }
             )
    def put(self, course_id, student_id):
        """
        Enrolling for a course
        """
        course = Course.get_by_id(course_id)
        student = User.get_by_id(student_id)
        #checks if student has been expelled
        if student.enrollment_status == EnrollmentStatus.EXPELLED:
            return {"message": "Student has been expelled. Cannot register for any course"}, HTTPStatus.BAD_REQUEST
        student.courses.append(course)

        db.session.commit()
        return student, HTTPStatus.OK
    

@blp.route("/course/<int:course_id>/unenroll/<int:student_id>")
class CourseUnEnroll(MethodView):
    @jwt_required()
    @admin_required()
    @blp.doc(description='Unenroll a student in a course. Can be accessed by only admins',
             params={
                "course_id": "The id of the course to unenroll for",
                "student_id": "The id of the student to unenroll"
             }
             )
    def put(self, student_id, course_id):
        """
        Unenroll a student from a course
        """
        course = Course.get_by_id(course_id)
        student = User.get_by_id(student_id)
        # checks if student has course registered
        if course in student.courses:
            student.courses.remove(course)
            # checks if the course has a score recorded
            score = Score.query.filter_by(user_id=student_id , course_id=course_id).first()
            if score:
                # deletes the score
                db.session.delete(score)
            db.session.commit()
            return {"Message": "Unenrolled student from course"}, HTTPStatus.OK
        return {"Error": "Student is not enrolled in this course"}, HTTPStatus.BAD_REQUEST


@blp.route("/courses/<path:student_id>")
class StudentCourseList(MethodView):
    @jwt_required()
    @blp.doc(description='Get all courses a student offers.'
              'This route can be accessed by an admin or the student whose id is in the student_id variable of the url.'
              'Student cannot access the route if expelled.',
             params={
                "student_id": "The student_id of the student"
             }
             )
    def get(self, student_id):
        """
        Get all courses a student offers
        """
        course_list = []
        identity = get_jwt_identity()
        user = User.get_by_id(identity)
        student = User.query.filter_by(student_id=student_id).first()
        
        # checks if student exists
        if student:
            # checks if the user accessing the route is an admin or the student whose course list is needed.
            if (user.is_admin == True) or (identity == student.id):
                for course in student.courses:
                    course_list.append(course.name)
                return jsonify(course_list), HTTPStatus.OK
            return {"message": "Not allowed."}, HTTPStatus.FORBIDDEN
        return {"message": "Student does not exist"}, HTTPStatus.NOT_FOUND


@blp.route("/course/<int:course_id>/students")
class CourseStudentsList(MethodView):
    @jwt_required()
    @admin_required()
    @blp.doc(description='Get the student id of all students that offers a course.'
              'This route can be accessed by only an admin.',
             params={
                "course_id": "The id of the course"
             }
             )
    def get(self, course_id):
        """
        Get all students that take a course
        """
        student_id_list = []
        course = Course.get_by_id(course_id)
        for student in course.users:
            student_id_list.append(student.student_id)
        return jsonify(student_id_list), HTTPStatus.OK
        

@blp.route("/course/<int:course_id>/score-upload")
class ScoreUpload(MethodView):
    @blp.arguments(ScoreUploadSchema)
    @jwt_required()
    @admin_required()
    @blp.doc(description='Upload the score of a student in a particular course.'
              'This route can be accessed by only an admin.',
             params={
                "course_id": "The id of the course"
             }
             )
    def put(self, result_data, course_id):
        """
        Upload course results
        """
        course = Course.get_by_id(course_id)
        student = User.query.filter_by(student_id=result_data['student_id']).first()
        # checks if student exists
        if student:
            score=result_data['score']

            # check for grades of score
            if score >= 70:
                grade = 'A'
            elif (score < 70 and score >= 60):
                grade = 'B'
            elif (score < 60 and score >=50):
                grade = 'C'
            elif (score < 50 and score >= 45):
                grade = 'D'
            elif (score < 45 and score >= 40):
                grade = 'E'
            else:
                grade = 'F'

            # checks if student is registered for the course
            if course in student.courses:
                existing_score = Score.query.filter_by(user_id=student.id, course_id=course_id).first()
                # checks if score exists and updates
                if existing_score:
                    existing_score.score = result_data['score']
                    existing_score.grade = grade
                    db.session.commit()
                    return {"message": "Result updated"}, HTTPStatus.ACCEPTED
                # creates score if it does not exist
                new_score = Score(score=result_data['score'], course_id=course_id, user_id=student.id, grade=grade)
                db.session.add(new_score)
                db.session.commit()
                return {"message": "Result uploaded"}, HTTPStatus.CREATED
            return {"message": "Student isn't registered for this course"}, HTTPStatus.BAD_REQUEST
        return {"Error": "Student does not exist"}, HTTPStatus.NOT_FOUND
        

        
            
