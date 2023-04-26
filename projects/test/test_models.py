from django.test import TestCase
from ..models import Project
from departaments.models import Departament

# Create your tests here.
class DepartamentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.departament = Departament.objects.create(**{"title": "Test Departament 01"})
        
        cls.dict_project = {
            "title": "My Project",
            "last_hours": "40:00:00",
            "departament": cls.departament
        }
        
            
    # def test_create_departament(self):
    #     project = Project.objects.create(**self.dict_project)
    #     self.assertEqual(project.title, self.dict_project["title"])
    #     self.assertEqual(project.estimed_hours, self.dict_project["estimed_hours"])
    #     self.assertEqual(project.last_hours, self.dict_project["last_hours"])
    #     self.assertEqual(project.departament.title, self.dict_project["departament"].title)
        
        
    # def test_create_departament_with_empty_title(self):
    #     departament = Employees.objects.create(**{"name": "", "username": "", "password": "", "cpf": "", "rg": "", "gender": "", "birth_date": "", "driver_license": "A", "salary": "", "weekly_hours": ""})
    #     self.assertEqual(departament.name, "")
    #     ...
    
    ...