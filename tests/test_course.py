import unittest
from app import create_app
from utils import db
from config.config import config_dict
from models.user import User
from models.courses import Course
from flask_jwt_extended import create_access_token

class CourseTestCase(unittest.TestCase):
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

    def test_get_courses(self):
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
        
        response = self.client.get('/course', headers=headers)

        assert response.json == []

        assert response.status_code == 200

    def test_post_course(self):
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

        response = self.client.post('/course', headers=headers, json=course_data)

        assert response.json["Unit"] == 1

        assert response.status_code == 201

    def test_get_course_by_id(self):
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

        self.client.post('/course', headers=headers, json=course_data)

        response = self.client.get('/course/1', headers=headers)

        assert response.status_code == 200

        assert response.json["teacher"] == "Prof"


    def test_enroll_student(self):
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

        self.client.post('/course', headers=headers, json=course_data)

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)

        student= User.query.filter_by(email='testuser@gmail.com').first()

        response = self.client.put('/course/1/enroll/2', headers=headers)

        assert response.status_code == 200

        assert response.json["id"] == student.id


    def test_unenroll_student(self):
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

        self.client.post('/course', headers=headers, json=course_data)

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)

        student= User.query.filter_by(email='testuser@gmail.com').first()

        response = self.client.put('/course/1/enroll/2', headers=headers)

        response = self.client.put('/course/1/unenroll/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {"Message": "Unenrolled student from course"}

    def test_student_course_list(self):
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
        response_final = self.client.get(f'/courses/{student.student_id}', headers=headers)

        assert response_final.status_code == 200
        assert len(response_final.json) == 2

    def test_course_student_list(self):
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
        self.client.post('/course', headers=headers, json=course_data)

        student_signup_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        
        student_signup_data_2 = {
            "first_name": "test",
            "last_name": "student",
            "email": "teststudent@gmail.com",
        }

        student_signup_data_3 = {
            "first_name": "test",
            "last_name": "student",
            "email": "testingstudent@gmail.com",
        }
        response = self.client.post('/students/signup', json=student_signup_data, headers=headers)
        response = self.client.post('/students/signup', json=student_signup_data_2, headers=headers)
        response = self.client.post('/students/signup', json=student_signup_data_3, headers=headers)

        response = self.client.put('/course/1/enroll/1', headers=headers)
        response = self.client.put('/course/1/enroll/2', headers=headers)
        response = self.client.put('/course/1/enroll/3', headers=headers)

        response_final = self.client.get('/course/1/students', headers=headers)

        assert response_final.status_code == 200
        assert len(response_final.json) == 3

    def test_score_upload(self):
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
        
        # student_score_data_2 = {
        #     "student_id": student.student_id,
        #     "score": 50,
        #     }
        
        response = self.client.put('/course/1/score-upload', headers=headers, json=student_score_data)

        assert response.json == {"message": "Result uploaded"}
        assert response.status_code == 201

