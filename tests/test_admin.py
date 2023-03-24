import unittest
from config.config import config_dict
from app import create_app
from utils import db
from models.user import User
from flask_jwt_extended import create_access_token

class AdminTestCase(unittest.TestCase):
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

    def test_change_admin_password(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "testadmin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = User.query.filter_by(email='testadmin@gmail.com').first()

        admin_change_password_data = {
                    "email": "testadmin@gmail.com",
                    "password": "adminte",
                    "new_password": "admin",
                    "confirm_new_password": "admin"
                }

        response = self.client.put('/admin/change_password', json=admin_change_password_data)

        assert response.status_code == 200

    def test_get_admins(self):
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
        
        response = self.client.get('/admin', headers=headers)

        assert response.status_code == 200

        assert len(response.json) == 1

    def test_delete_admin(self):
        admin_signup_data = {
                    "first_name": "Test",
                    "last_name": "Admin",
                    "email": "promiseanuoluwa@gmail.com"
                }
        
        admin_signup_data_2 = {
                    "first_name": "Test2",
                    "last_name": "Admin",
                    "email": "admin@gmail.com"
                }

        response = self.client.post('/admin/signup', json=admin_signup_data)
        response = self.client.post('/admin/signup', json=admin_signup_data_2)

        admin = User.query.filter_by(email='promiseanuoluwa@gmail.com').first()

        token = create_access_token(identity=admin.id, additional_claims={"is_administrator": True}, fresh=True)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.delete('/admin/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {"message": "Admin deleted"}

