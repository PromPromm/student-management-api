import unittest
from app import create_app
from utils import db
from config.config import config_dict
from models.user import User
from models.courses import Course
from flask_jwt_extended import create_access_token

class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()


    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_get_students(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/student', headers=headers)

        assert response.status_code == 200

        assert response.json == []

    def test_get_student_by_id(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=data, headers=headers)

        response = self.client.get('/student/2', headers=headers)

        assert response.status_code == 200

        assert response.json["email"] == 'testuser@gmail.com'

    def test_change_enrollment_status(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=data, headers=headers)

        enrol_data = {
            "enrollment_status" : "expelled"
        }

        response = self.client.put('/student/2', headers=headers, json=enrol_data)

        assert response.status_code == 200

        assert response.json["enrollment_status"] == 'expelled'

    def test_delete_student(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True}, fresh=True)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=data, headers=headers)

        response = self.client.delete('/student/2', headers=headers)

        assert response.json == {"message": "Student deleted"}

        assert response.status_code == 200


    def test_change_student_password(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)

        student= User.query.filter_by(email='testuser@gmail.com').first()

        student_change_password_data = {
                    "student_id": student.student_id,
                    "password": "userte",
                    "new_password": "student",
                    "confirm_new_password": "student"
                }

        response = self.client.put('/student/change_password', json=student_change_password_data)

        assert response.json == {"message": "Password successfully changed. Proceed to login"}

        assert response.status_code == 200

    def test_student_score_list(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        course_data = {
            "name": "Physics",
            "teacher": "Prof",
            "unit": 1
        }
        course_data_2 = {
            "name": "Soft skills",
            "teacher": "Fope Daniels",
            "unit": 4
        }

        self.client.post('/course', headers=headers, json=course_data)
        self.client.post('/course', headers=headers, json=course_data_2)

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)

        student= User.query.filter_by(email='testuser@gmail.com').first()

        response = self.client.put('/course/1/enroll/2', headers=headers)
        response = self.client.put('/course/2/enroll/2', headers=headers)
        
        student_score_data = {
            "student_id": student.student_id,
            "score": 70,
            }
        
        student_score_data_2 = {
            "student_id": student.student_id,
            "score": 50,
            }
        
        response = self.client.put('/course/1/score-upload', headers=headers, json=student_score_data)
        response = self.client.put('/course/2/score-upload', headers=headers, json=student_score_data_2)

        response = self.client.get(f'/student/{student.student_id}/scores', headers=headers)

        assert response.status_code == 200
        assert len(response.json) == 2

    def test_student_cgpa(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }

        course_data = {
            "name": "Physics",
            "teacher": "Prof",
            "unit": 1
        }
        course_data_2 = {
            "name": "Soft skills",
            "teacher": "Fope Daniels",
            "unit": 4
        }

        self.client.post('/course', headers=headers, json=course_data)
        self.client.post('/course', headers=headers, json=course_data_2)

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)

        student= User.query.filter_by(email='testuser@gmail.com').first()

        response = self.client.put('/course/1/enroll/2', headers=headers)
        response = self.client.put('/course/2/enroll/2', headers=headers)
        
        student_score_data = {
            "student_id": student.student_id,
            "score": 70,
            }
        
        student_score_data_2 = {
            "student_id": student.student_id,
            "score": 50,
            }
        
        response = self.client.put('/course/1/score-upload', headers=headers, json=student_score_data)
        response = self.client.put('/course/2/score-upload', headers=headers, json=student_score_data_2)

        response = self.client.get(f'/student/{student.student_id}/cgpa', headers=headers)

        assert response.status_code == 200

    