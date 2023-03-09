from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from models.user import User
from schemas import UserSchema, AdminChangePasswordSchema
from utils import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required

blp = Blueprint("admins", __name__, description='Operations on admins')

@blp.route('/admin/change_password')
class AdminChangePassword(MethodView):
    @blp.arguments(AdminChangePasswordSchema)
    @blp.response(200, UserSchema)
    def patch(self, user_data):
        """
        Endpoint for admin to change the automatically generated password
        """
        user = User.query.filter_by(email=user_data['email']).first()

        if user and check_password_hash(user.password, user_data["password"]):
            if user_data["new_password"] == user_data["confirm_new_password"]:
                user.password = generate_password_hash(user_data["new_password"])
                db.session.commit()
                return user
            abort(401, "New password and confirm password do not match")
        abort(401, 'Invalid credentials')


@blp.route("/admin")
class AdminList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """
        Get all administrators
        """
        admins = User.query.filter(User.is_admin == True)
        return admins
    


@blp.route("/admin/<int:admin_id>")
class Admin(MethodView):
    @jwt_required()
    def delete(self, admin_id):
        """
        Delete an admin by id
        """
        user = User.get_by_id(admin_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "Admin deleted"}
