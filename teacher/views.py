from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("teachers", __name__, description='Operations on teachers')

@blp.route("/teacher")
class TeacherList(MethodView):
    def get(self):
        """
        Get all teachers
        """
        pass


@blp.route('/teacher/<int:teacher_id>')
class Teacher(MethodView):
    def get(self, teacher_id):
        """
        Get a teacher by id
        """
        pass


    def patch(self, teacher_id):
        """
        Update the courses a teacher takes
        """
        pass

    def delete(self, teacher_id):
        """
        Delete teacher by id
        """
        pass


