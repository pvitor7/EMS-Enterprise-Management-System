from django.test import TestCase
from ..models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = {
            "username": "userone",
            "password": "s3nh4s3gur4",
            "email": "one.special@mail.com",
            "cellphone": "11999999999"
            }

    def test_db_create_user(self):
        user_created = User.objects.create_user(**self.user)
        get_user = User.objects.all()[0]
        self.assertEqual(user_created, get_user)
