from utils import db

class Course(db.Model):
    __tablename__='course'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    teacher = db.Column(db.String(45), nullable=False)
    

    def __repr__(self):
        return f'<Course {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
