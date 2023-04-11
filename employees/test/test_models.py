from django.test import TestCase
from ..models import Employees

# Create your tests here.
class DepartamentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dict_employee = {
            "name": "João da Silva",
            "cpf": "12345678901",
            "rg": "12345678-9",
            "gender": "Male",
            "driver_license": "B",
            "birth_date": "1990-01-01",
            "salary": 2000.00,
            "weekly_hours": "20:00",
            "created_at": "2022-04-11T14:30:00Z",
            "updated_at": "2022-04-11T14:30:00Z"
        }
        
            
    def test_create_departament(self):
        departament = Employees.objects.create(**self.dict_employee)
        self.assertEqual(departament.name, self.dict_employee["name"])
        self.assertEqual(departament.cpf, self.dict_employee["cpf"])
        self.assertEqual(departament.rg, self.dict_employee["rg"])
        self.assertEqual(departament.gender, self.dict_employee["gender"])
        self.assertEqual(departament.birth_date, self.dict_employee["birth_date"])
        self.assertEqual(departament.driver_license, self.dict_employee["driver_license"])
        self.assertEqual(departament.salary, self.dict_employee["salary"])
        self.assertEqual(departament.weekly_hours, self.dict_employee["weekly_hours"])
        
        
    # def test_create_departament_with_empty_title(self):
    #     departament = Employees.objects.create(**{"name": "", "username": "", "password": "", "cpf": "", "rg": "", "gender": "", "birth_date": "", "driver_license": "A", "salary": "", "weekly_hours": ""})
    #     self.assertEqual(departament.name, "")
    #     ...
    
    ...