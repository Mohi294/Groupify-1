from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer

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


