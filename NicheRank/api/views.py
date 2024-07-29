from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer
from .models import userInfo
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class UserView(generics.ListAPIView):
    queryset = userInfo.objects.all()
    serializer_class = UserSerializer
    


