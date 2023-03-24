import unittest
from config.config import config_dict
from app import create_app
from utils import db
from models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthenticationTestCase(unittest.TestCase):
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

    def test_student_registration(self):
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com"
        }

        # creates admin
        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        # create a jwt token with admin id
        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True})

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            }
        # test student signup
        response = self.client.post('/students/signup', json=data, headers=headers)

        user = User.query.filter_by(email="testuser@gmail.com").first()

        assert user.first_name == "test"

        assert response.status_code == 201

        assert user.is_admin == False

        # test student login
        student_login_data = {
            "student_id": user.student_id,
            "password": "userte"
        }

        response = self.client.post('/student/login', json=student_login_data)

        assert response.status_code == 200



    def test_admin_registration(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        assert admin.is_admin == True

        assert response.status_code == 201

    
    def test_admin_login(self):
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com"
        }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        data = {
            "email": "testadmin@gmail.com",
            "password": "adminte"
        }

        response = self.client.post('/admin/login', json=data)

        assert response.status_code == 200

    def test_user_refresh(self):
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com"
        }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_refresh_token(identity=admin.id)
        header = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post('/refresh', headers=header)

        assert response.status_code == 200

    def test_user_logout(self):
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com"
        }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id, fresh=True)

        header = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.delete('/logout', headers=header)
        assert response.status_code == 200
        assert response.json == {"message": "User successfully logged out"}
