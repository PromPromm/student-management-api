from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("auth", __name__, description='Authentication and Authorization Operations')


@blp.route('/signup')
class UserRegister(MethodView):
    def post(self):
        """
        Register a user, student or teacher
        """
        pass


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

