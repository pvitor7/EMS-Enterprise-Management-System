from django.test import TestCase
from ..models import Departament, Roles

# Create your tests here.
class DepartamentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dict_departament = {"title": "Test Departament 01"};
        
    def test_create_departament(self):
        departament = Departament.objects.create(**self.dict_departament)
        self.assertEqual(departament.title, self.dict_departament["title"])
        
    def test_create_departament_with_empty_title(self):
        departament = Departament.objects.create(**{"title": ""})
        self.assertEqual(departament.title, "")
