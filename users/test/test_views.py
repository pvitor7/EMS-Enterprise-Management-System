from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import User
from django.urls import reverse


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.client: APIClient;
        
        cls.test_user = User.objects.create_user(**{
            "username": "usertest",
            "password": "s3nh4s3gur4",
            "email": "user.test@mail.com",
            "cellphone": "11999999900"})
        
                
        cls.user_1 = {
            "username": "userone",
            "password": "s3nh4s3gur4",
            "email": "one.special@mail.com",
            "cellphone": "11999999999"
            }
        
        cls.test_login = {
            "username": "usertest",
            "password": "s3nh4s3gur4"
            }
        
        cls.base_create_user_url = reverse("user-create-view")
        cls.base_login_url = reverse("login-view")
        cls.base_user_retrive_url = reverse("user-retrive-view", kwargs={'pk': cls.test_user.id})
        cls.base_list_users_url = reverse("list-users-view")
        


    def test_empty_create_user(self):
        test_request = {}
        expected_status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.base_create_user_url, data=test_request)
        self.assertEquals(expected_status_code, response.status_code)


    def test_create_user(self):
        expected_status_code = status.HTTP_201_CREATED
        response = self.client.post(self.base_create_user_url, self.user_1);
        self.assertEquals(response.status_code, expected_status_code)


    def test_login_username_user(self):
        expected_status_code = status.HTTP_200_OK
        response = self.client.post(self.base_login_url, self.test_login)
        self.assertEquals(response.status_code, expected_status_code)


    def test_retrive_user_with_empty_token(self):
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        response = self.client.get(self.base_user_retrive_url)
        self.assertEquals(response.status_code, expected_status_code)
    

    def test_retrive_user(self):
        response_login = self.client.post(self.base_login_url, self.test_login)
        token = response_login.data['token'];
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        expected_status_code = status.HTTP_200_OK
        response = self.client.get(self.base_user_retrive_url)
        self.assertEquals(response.status_code, expected_status_code)
    

    def test_update_cellphone_user(self):
        response_login = self.client.post(self.base_login_url, self.test_login)
        token = response_login.data['token'];
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        dict_update = {"cellphone": "2199885599"}
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(self.base_user_retrive_url, dict_update)
        self.assertEquals(response.status_code, expected_status_code)
        self.assertEquals(response.data['id'], str(self.test_user.id))
        self.assertEquals(response.data['cellphone'], dict_update['cellphone'])
    

    def test_delete_user(self):
        response_login = self.client.post(self.base_login_url, self.test_login)
        token = response_login.data['token'];
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        expected_status_code = status.HTTP_204_NO_CONTENT
        response = self.client.delete(self.base_user_retrive_url)
        self.assertEquals(response.status_code, expected_status_code)