
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, UserSerializer
from rest_framework import generics
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import Request, Response, APIView
from django.http import Http404
from rest_framework.authtoken.models import Token
from .permissions import UserAccount


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class UserListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserAccount]
    queryset = User.objects.all()
    serializer_class = UserSerializer


    
class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    
    def post(self, request: Request) -> Response:
        user_dict = request.data
        
        if request.data.get('email'):
            username = get_object_or_404(
            User, email=request.data['email']).username
            user_dict['username'] = username

        elif request.data.get('cellphone'):
            username = get_object_or_404(
            User, cellphone=request.data['cellphone']).username
            user_dict['username'] = username
        
        serializer = LoginSerializer(data=user_dict)
        serializer.is_valid(raise_exception=True)
        login_user = authenticate(**serializer.validated_data)
        if not login_user:
            raise Http404("User not found.")
        token, _ = Token.objects.get_or_create(user=login_user)
        return Response({"token": token.key})
        