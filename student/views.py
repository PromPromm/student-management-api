from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, EnrollmentStatus, student_course
from schemas import UserSchema, StudentChangePasswordSchema, ChangeEnrollmentStatusSchema
from utils import db
from werkzeug.security import check_password_hash, generate_password_hash
from utils import admin_required, grade_to_point_converter
from http import HTTPStatus
from models.courses import Course
from models.scores import Score

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


    @blp.doc(description='Update a student enrollment by id. Can be accessed by only an admin.'
             ' The enrollment can either be "active", "in_waitlist" or "expelled"',
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
                return {"message": "Password successfully changed. Proceed to login"}, HTTPStatus.OK
            return {"Error": "New password and confirm password do not match"}, HTTPStatus.BAD_REQUEST
        return {"Error": "Invalid credentials"}, HTTPStatus.FORBIDDEN


@blp.route('/student/<path:student_id>/scores')
class StudentScoreList(MethodView):
    @jwt_required()
    @blp.doc(description='Get all the scores of a student in each course.'
              'This route can be accessed by an admin or the student whose id is in the student_id variable of the url.'
              'Student cannot access the route if expelled.',
             params={
                "student_id": "The student_id of the student"
             }
             )
    def get(self, student_id):
        """
        Get student scores and grades
        """
        identity = get_jwt_identity()
        user = User.get_by_id(identity)
        
        score_course_list = []
        student = User.query.filter_by(student_id=student_id).first()
        # check if student exists
        if student:
            # checks if the user accessing the route is an admin or the student whose course list is needed.
            if (user.is_admin == True) or (identity == student.id):
                    for course in student.courses:
                        score_in_course = {}
                        score = Score.query.filter_by(user_id=student.id , course_id=course.id).first()
                        score_in_course['name'] = course.name
                        # checks if the course has a score
                        if score:
                            score_in_course['score'] = score.score
                            score_in_course['grade'] = score.grade
                        else:
                            score_in_course['score'] = None
                            score_in_course['grade'] = None
                        score_course_list.append(score_in_course)
                    return score_course_list, HTTPStatus.OK
            return {"message": "Not allowed."}, HTTPStatus.FORBIDDEN
        return {"message": "Student does not exist"}, HTTPStatus.NOT_FOUND  


@blp.route('/student/<path:student_id>/cgpa')
class StudentCGPA(MethodView):
    @jwt_required()
    @blp.doc(description='Get all the gpa of a student.'
              'This route can be accessed by an admin or the student whose id is in the student_id variable of the url.'
              'Student cannot access the route if expelled.',
             params={
                "student_id": "The student_id of the student"
             }
             )
    def get(self, student_id):
        """
        Get student gpa
        """
        identity = get_jwt_identity()
        user = User.get_by_id(identity)
        student = User.query.filter_by(student_id=student_id).first()
        # checks if student exists
        if student:
            # checks if the user accessing the route is an admin or the student whose course list is needed.
            if (user.is_admin == True) or (identity == student.id):
                courses = Course.query.join(student_course).join(User).filter(User.id == student.id).all()
                total_credit_units = 0
                obtained_score = 0
                for course in courses:
                    score = Score.query.filter_by(user_id=student.id , course_id=course.id).first()
                    # checks if score exists
                    if score:
                        score_grade = grade_to_point_converter(score.grade)
                        total_credit_units += course.unit
                        obtained_score += (course.unit * score_grade)

                # checks if the student has no score in any course
                if total_credit_units == 0:
                    return {
                        'message':'Student has no score. Try uploading a score!.'}, HTTPStatus.OK
                gpa = round( (obtained_score / total_credit_units), 2)
                return {
                    'message': f'GPA for {student_id} is {gpa}'}, HTTPStatus.OK
            return {"message": "Not allowed."}, HTTPStatus.FORBIDDEN
        return {"message": "Student does not exist"}, HTTPStatus.NOT_FOUND
        

