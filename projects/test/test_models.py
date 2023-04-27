from django.test import TestCase
from ..models import Project
from users.models import User
from departaments.models import Departament
from datetime import date, timedelta
from django.core.exceptions import ValidationError


# Create your tests here.
class DepartamentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = {
            "username": "userone",
            "password": "s3nh4s3gur4",
            "email": "one.special@mail.com",
            "cellphone": "11999999999"
            }
        
        cls.user_created = User.objects.create_user(**cls.user)
        
        cls.departament = Departament.objects.create(**{"title": "Test Departament 01"})
        
        
            
    def test_create_departament(self):
        project = Project.objects.create(
            title='Project Test',
            estimed_date=date.today() + timedelta(days=7),
            departament=self.departament
        )
        self.assertEqual(project.title, 'Project Test')
        self.assertEqual(project.estimed_date, date.today() + timedelta(days=7))
        self.assertEqual(project.departament, self.departament)
