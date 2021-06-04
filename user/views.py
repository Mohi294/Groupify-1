from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model, authenticate
from user.serializers import UserSerializer, ChangePasswordSerializer,UpdateUserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# for test
def hello(request):
    return HttpResponse("hello world")

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = UserSerializer


class ChangePasswordView(generics.UpdateAPIView):

    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):

    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
