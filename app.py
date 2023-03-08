from flask import Flask
from flask_smorest import Api
from config import config_dict
from auth import blp as AuthBlueprint
from courses import blp as CourseBlueprint
from student import blp as StudentBlueprint
from flask_migrate import Migrate
from utils import db
from models.courses import Course
from models.user import User
from models.blocklist import TokenBlocklist
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(CourseBlueprint)
    api.register_blueprint(StudentBlueprint)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'user': User,
            'course': Course
        }

    return app
