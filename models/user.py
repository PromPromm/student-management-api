from utils import db
from enum import Enum
from datetime import datetime

student_course = db.Table('user_course',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
                    )

class EnrollmentStatus(Enum):
    ACTIVE = 'active'
    WAITLIST = 'in_waitlist'
    EXPELLED = 'expelled'
    ADMIN = 'admin'
    

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    student_id =db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    enrollment_status = db.Column(db.Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.WAITLIST)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    courses = db.relationship('Course', secondary=student_course, backref='users')
    scores = db.relationship('Score', backref='user')

    def __repr__(self):
        return f'<User {self.student_id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def make_admin(self):
        """
        Gives user admin privileges
        """
        self.is_admin = True
        db.session.commit()