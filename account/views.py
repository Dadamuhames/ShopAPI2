from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from rest_framework import views, viewsets, generics, status
from .serializers import LoginSerializer, UserInformationSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .models import User
import random


# Check number
class CheckNubmer(views.APIView):
    def get(self, request, format=None):
        nbm = request.data.get('nbm')

        if nbm is None:
            return Response({'error': 'Number is required'})

        users = User.objects.filter(is_active=True)

        data = {
            'is_user': nbm in [it.nbm for it in users]
        }

        return Response(data)


# send sms
class SendSms(views.APIView):
    def post(self, request, format=None):
        nbm = request.data.get("nbm")

        if nbm is None:
            return Response({'error': 'Number is required'})

        code = random.randint(100000, 999999)
        print(nbm, code)

        return Response({'nbm': nbm, 'code': code})


# check code
#  
        

# Dashboard
class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = UserInformationSerializer(request.user).data
        return Response(user)



# Sing Up
class SingUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInformationSerializer
