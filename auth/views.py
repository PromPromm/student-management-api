from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import PlainUserSchema, StudentLoginSchema, AdminLoginSchema
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, EnrollmentStatus
from utils import db, generate_student_id
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models.blocklist import TokenBlocklist
from datetime import datetime, timezone
from http import HTTPStatus
from utils import admin_required, super_admin_required

blp = Blueprint("auth", __name__, description='Authentication and Authorization Operations')


@blp.route('/students/signup')
class StudentRegister(MethodView):
    @admin_required()
    @jwt_required()
    @blp.arguments(PlainUserSchema)
    @blp.doc(description="This route can be accessed only by an administrator")
    def post(self, user_data):
        """
        Registers a student
        """
        user = User.query.filter_by(email=user_data['email']).first()
        # checks if user exists
        if user:
            return {"Error": "User exists"}, HTTPStatus.CONFLICT
        # generate the default user password
        password = (user_data["last_name"] + user_data["first_name"][0:2]).lower()
        # create new user[student]
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=generate_password_hash(password),
            student_id=generate_student_id()
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Student successfully created", "student_id": new_user.student_id}, HTTPStatus.CREATED
    

@blp.route('/admin/signup')
class AdminRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    # @super_admin_required()
    @blp.doc(description="This route can be accessed only by the SUPER administrator")
    def post(self, user_data):
        """
        Register an admin
        """
        user = User.query.filter_by(email=user_data['email']).first()
        # checks if user exists
        if user:
            return {"Error": "User exists"}, HTTPStatus.CONFLICT
        # generate the default user password
        password = (user_data["last_name"] + user_data["first_name"][0:2]).lower()
        # create new user[admin]
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=generate_password_hash(password),
            enrollment_status='ADMIN',
            is_admin=True
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Admin successfully created"}, HTTPStatus.CREATED


@blp.route('/student/login')
class StudentLogin(MethodView):
    @blp.arguments(StudentLoginSchema)
    @blp.doc(description="Logs in a student and generates a jwt access token. Student cannot access this route if expelled.")
    def post(self, user_data):
        """
        Login a student and generate access token
        """
        user = User.query.filter_by(student_id=user_data["student_id"]).first()

        # checks if student exists and if the password entered is the same as the one saved in the database.
        if user and check_password_hash(user.password, user_data["password"]):
            # checks if user has been expelled
            if user.enrollment_status == EnrollmentStatus.EXPELLED:
                return {"Error": "You are no longer a student"}, HTTPStatus.UNAUTHORIZED
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims={"is_administrator": False})
            refresh_token = create_refresh_token(identity=user.id, additional_claims={"is_administrator": False})
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        return {"Error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED


@blp.route('/admin/login')
class AdminLogin(MethodView):
    @blp.arguments(AdminLoginSchema)
    @blp.doc(description="Logs in an admin and generates a jwt access token")
    def post(self, user_data):
        """
        Login admin and generate access token
        """
        user = User.query.filter_by(email=user_data["email"]).first()

        # checks if admin exists and if the password entered is the same as the one saved in the database.
        if user.is_admin and check_password_hash(user.password, user_data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims={"is_administrator": True})
            refresh_token = create_refresh_token(identity=user.id, additional_claims={"is_administrator": True})
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        return {"Error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
        

@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.doc(description="Generates a refresh jwt access token")
    def post(self):
        """
        Generates refresh token
        """
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        if user.is_admin:
            access_token = create_access_token(identity=user_id, fresh=False, additional_claims={"is_administrator": True})
            return {"access_token": access_token}, HTTPStatus.OK
        access_token = create_access_token(identity=user_id, fresh=False, additional_claims={"is_administrator": False})
        return {"access_token": access_token}, HTTPStatus.OK
    

@blp.route('/logout')
class Logout(MethodView):
    @jwt_required(fresh=True)
    @blp.doc(description="Logs out user and revokes jwt")
    def delete(self):
        """
        Logout a user and blacklist jwt token
        """
        jti = get_jwt()["jti"]
        token = TokenBlocklist(jti=jti, created_at=datetime.now(timezone.utc))
        db.session.add(token)
        db.session.commit()
        return {"message": "User successfully logged out"}, HTTPStatus.OK
        