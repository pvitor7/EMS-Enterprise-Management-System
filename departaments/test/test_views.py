from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ..models import Departament

# Create your tests here.
class DepartamentModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient;
        
        cls.test_user = User.objects.create_user(**{
            "username": "usertest",
            "password": "s3nh4s3gur4",
            "email": "user.test@mail.com",
            "cellphone": "11999999900"})
        
        cls.token = Token.objects.create(user=cls.test_user).key
        
        cls.departament = Departament.objects.create(**{"title": "Test Departament"});
        
        cls.dict_departament = {"title": "Test Departament 01"};
        
        cls.base_create_departaments_url = reverse("departament-list-create-view")
        cls.base_departament_retrive_url = reverse("departament-retrive-view", kwargs={'pk': cls.departament.id})
        
        
    def test_create_departament_with_invalid_token(self):
        test_request = {"title": "Departament Token Inválido"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'Invalid')
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        response = self.client.post(self.base_create_departaments_url, test_request)
        self.assertEquals(expected_status_code, response.status_code)   
    
    
    def test_empty_create_departament(self):
        test_request = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        expected_status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.base_create_departaments_url, test_request)
        self.assertEquals(expected_status_code, response.status_code)
        
        
    def test_create_departaments(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        expected_status_code = status.HTTP_201_CREATED
        response = self.client.post(self.base_create_departaments_url, self.dict_departament)
        self.assertEquals(expected_status_code, response.status_code)
        
        
    def test_retrive_departament(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        expected_status_code = status.HTTP_200_OK
        response = self.client.get(self.base_departament_retrive_url)
        self.assertEquals(response.status_code, expected_status_code)
        
        
    def test_update_departament(self):
        update_dict = {"title": "Departament Update"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(self.base_departament_retrive_url, update_dict)
        self.assertEquals(response.data['title'], update_dict['title'])
        self.assertEquals(response.status_code, expected_status_code)
        
        
    def test_delete_departament(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        expected_status_code = status.HTTP_204_NO_CONTENT
        response = self.client.delete(self.base_departament_retrive_url)
        self.assertEquals(response.status_code, expected_status_code)