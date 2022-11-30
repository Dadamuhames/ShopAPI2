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
        code = random.randint(100000, 999999)
        print(code)
        




# Create your views here.
class LoginView(views.APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = ()

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            vd = serializer.validated_data
            user = authenticate(username=vd['nbm'], password=vd['password'])
            
            if user is None:
                return Response({'error': 'Password or number is invalid.'})

    
            login(request, user)


        else:
            return Response(serializer.errors)
        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name
        }, status=status.HTTP_200_OK)


    def get(self, request, format=None):
        serializer = LoginSerializer()

        print(serializer.data)

        return Response(serializer.data)


# Dashboard
class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = UserInformationSerializer(request.user).data
        return Response(user)



# Sing Up
class SingUpView(generics.CreateAPIView):
    queryset = User.object.all()
    #serializer_class = 