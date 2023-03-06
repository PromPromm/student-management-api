from flask import Flask
from flask_smorest import Api
from config import config_dict
from auth import blp as AuthBlueprint
from courses import blp as CourseBlueprint
from teacher import blp as TeacherBlueprint
from student import blp as StudentBlueprint


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    api = Api(app)

    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(CourseBlueprint)
    api.register_blueprint(TeacherBlueprint)
    api.register_blueprint(StudentBlueprint)

    return app
