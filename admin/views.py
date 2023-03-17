from flask.views import MethodView
from flask_smorest import Blueprint
from models.user import User
from schemas import UserSchema, AdminChangePasswordSchema
from utils import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required
from utils import admin_required, super_admin_required
from http import HTTPStatus

blp = Blueprint("admins", __name__, description='Operations on admins')

@blp.route('/admin/change_password')
class AdminChangePassword(MethodView):
    @blp.arguments(AdminChangePasswordSchema)
    @blp.doc(description='Change admin password. Can be accessed by only an admin')
    # @blp.response(200, UserSchema)
    def put(self, user_data):
        """
        Admin change password route
        """
        user = User.query.filter_by(email=user_data['email']).first()

        # checks if user exists and password matches
        if user and check_password_hash(user.password, user_data["password"]):
            # check if the new_password field and confirm_new_password field is the same
            if user_data["new_password"] == user_data["confirm_new_password"]:
                user.password = generate_password_hash(user_data["new_password"])
                db.session.commit()
                return {"message": "Password successfully changed. Proceed to login"}, HTTPStatus.OK
            return {"Error": "New password and confirm password do not match"}, HTTPStatus.BAD_REQUEST
        return {"Error": "Invalid credentials"}, HTTPStatus.FORBIDDEN


@blp.route("/admin")
class AdminList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.doc(description='Retrieve all administrators. This method can be accessed by only an admin')
    @jwt_required()
    @admin_required()
    def get(self):
        """
        Get all administrators
        """
        admins = User.query.filter(User.is_admin == True)
        return admins, HTTPStatus.OK
    

@blp.route("/admin/<int:admin_id>")
class Admin(MethodView):
    @jwt_required(fresh=True)
    @super_admin_required()
    @blp.doc(description='Delete an administrator by id. This method can be accessed by only the SUPER admin. Takes a fresh jwt access token',
             params= {
                        'admin_id': "The id of the admin to delete"
                            }
             )
    def delete(self, admin_id):
        """
        Delete an admin by id
        """
        user = User.get_by_id(admin_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "Admin deleted"}, HTTPStatus.OK
