from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from schemas import PlainUserSchema
from werkzeug.security import generate_password_hash
from models.user import User
from utils import db, generate_student_id

blp = Blueprint("auth", __name__, description='Authentication and Authorization Operations')


@blp.route('/signup')
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        """
        Register a user, student
        """
        user = User.query.filter_by(email=user_data['email']).first()
        if user:
            abort(409, 'This user already exists')
        password = user_data["last_name"] + user_data["first_name"][0:2]
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=generate_password_hash(password),
            student_id=generate_student_id()
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User successfully created", "student_id": new_user.student_id, "password": new_user.password}, 201



@blp.route('/login')
class UserLogin(MethodView):
    def post(self):
        """
        Login a user and generate access token
        """
        pass


@blp.route('/refresh')
class TokenRefresh(MethodView):
    def post(self):
        """
        Generates refresh token
        """
        pass

@blp.route('/logout')
class Logout(MethodView):
    def delete(self):
        """
        Logouts a user and blacklist jwt token
        """
        pass

