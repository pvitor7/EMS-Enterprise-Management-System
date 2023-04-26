from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from ..models import User
from rest_framework.authtoken.models import Token


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_pk= {
            "username": "Pk User",
            "password": "s3nh4s3gur4",
            "email": "pkuser@mail.com",
            "cellphone": "21992248141" 
        }
        
        cls.client = APIClient()
        cls.base_create_user_url = reverse("user-create-view")
        cls.base_login_url = reverse("login-view")
        cls.base_list_users_url = reverse("list-users-view")
        
        
        cls.user_1 = {
            "username": "userone",
            "password": "s3nh4s3gur4",
            "email": "one.special@mail.com",
            "cellphone": "11999999999"
            }
        
        cls.user_2 = {
            "username": "usertwo",
            "password": "s3nh4s3gur4",
            "email": "two.special@mail.com",
            "cellphone": "21999999999"
        }
        
        cls.login = {"username": cls.user_1['username'], 'password': cls.user_1['password']}
        
        cls.token = None
        cls.user = None
        
    def authenticate(self):
        self.token = self.client.post(self.base_login_url, self.login).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.user = User.objects.get(username=self.login['username'])
    
    def test_empty_create_user(self):
        test_request = {}
        expected_status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.base_create_user_url, data=test_request)
        self.assertEquals(expected_status_code, response.status_code)
        
    def test_create_user_owner(self):
        expected_status_code = status.HTTP_201_CREATED
        response = self.client.post(self.base_create_user_url, self.user_1)
        self.assertEquals(response.status_code, expected_status_code)
        
    def test_login_username_owner(self):
        self.client.post(self.base_create_user_url, self.user_1)
        expected_status_code = status.HTTP_200_OK
        response = self.client.post(self.base_login_url, self.login)
        self.assertEquals(response.status_code, expected_status_code)
    
    def test_list_users(self):
        self.client.post(self.base_create_user_url, self.user_1)
        self.authenticate()
        expected_status_code = status.HTTP_200_OK
        response = self.client.get(self.base_list_users_url)
        self.assertEquals(response.status_code, expected_status_code)
        
    def test_list_users_without_token(self):
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        response = self.client.get(self.base_list_users_url)
        self.assertEquals(response.status_code, expected_status_code)
        
    def test_retrieve_user(self):
        self.client.post(self.base_create_user_url, self.user_1)
        self.authenticate()
        expected_status_code = status.HTTP_200_OK
        response = self.client.get(reverse("user-detail-view", kwargs={"pk": self.user.pk}))
        self.assertEquals(response.status_code, expected_status_code)
        
        
    def test_update_user(self):
        self.client.post(self.base_create_user_url, self.user_1);
        login = {"username": self.user_1['username'], 'password': self.user_1['password']}
        token = self.client.post(self.base_login_url, login).data['token']
        user = User.objects.get(username=self.user_1['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {"cellphone": "11988888888"}
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(reverse("user-detail-view", kwargs={"pk": user.pk}), data=data)
        self.assertEquals(response.status_code, expected_status_code)
        user.refresh_from_db()
        self.assertEquals(user.cellphone, data['cellphone'])
        
    def test_delete_user(self):
        self.client.post(self.base_create_user_url, self.user_1);
        login = {"username": self.user_1['username'], 'password': self.user_1['password']}
        token = self.client.post(self.base_login_url, login).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        user = User.objects.get(username=self.user_1['username'])
        expected_status_code = status.HTTP_204_NO_CONTENT
        response = self.client.delete(reverse("user-detail-view", kwargs={"pk": user.pk}))
        self.assertEquals(response.status_code, expected_status_code)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.pk)