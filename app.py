from flask import Flask, jsonify
from flask_smorest import Api
from config import config_dict
from auth import blp as AuthBlueprint
from courses import blp as CourseBlueprint
from student import blp as StudentBlueprint
from admin import blp as AdminBlueprint
from flask_migrate import Migrate
from utils import db
from models.courses import Course
from models.user import User
from models.scores import Score
from models.blocklist import TokenBlocklist
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired",
                    "error": "token_expired"
                }
            ), 401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "description": "The token is not fresh",
                "error": "fresh_token_required"
            }
        ), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed",
                    "error": "invalid_token"
                }
            ), 401
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required"
                }
            ), 401
        )


    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(CourseBlueprint)
    api.register_blueprint(StudentBlueprint)
    api.register_blueprint(AdminBlueprint)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'user': User,
            'course': Course
        }

    return app
