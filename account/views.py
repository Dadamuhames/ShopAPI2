from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import views, viewsets, generics, status
from .serializers import LoginSerializer, UserInformationSerializer, PasswordSerializer, UserUpdateSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
import random
import datetime
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from django.core.cache import cache

# Check number
class CheckNubmer(views.APIView):
    def post(self, request, format=None):
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

        
        #code = random.randint(100000, 999999)
        if not self.request.session.session_key:
            self.request.session.cycle_key()
        
        code = 666666
        cache.set(nbm, {
            'code': str(code),
            'counter': 1
        }, 5 * 60)


        print(nbm, code)

        return Response(cache.get(str(self.request.session.session_key)))


# check code
class CodeValidate(views.APIView):
    def post(self, request, format=None):
        if not self.request.session.session_key:
            return Response({'error': 'cashe is clean'})

        my_cache = cache.get(str(self.request.session.session_key), {})
        code = request.data.get("code")
        in_cache_code = my_cache.get('code')


        if code is None or  in_cache_code is None:
            return Response({'error': 'Code is requiered'}, status=status.HTTP_403_FORBIDDEN)


        _bool = code == in_cache_code

        data = {
            'correct': _bool
        }

        if my_cache.get('user') is not None:
            id = my_cache['user']
            data['user'] = User.objects.get(id=int(id))

        return Response(data)


# verify with code
# set code as user password
class ChangeUser(views.APIView):
    def post(self, request, format=None):
        nbm = request.POST.get('nbm')
        user = get_object_or_404(User.objects.filter(is_active=True), nbm=nbm)

        if request.data.get("password"):
            user.set_password(request.data.get("password"))
            user.save()
        else:
            return Response({'error': 'Passwords  is invalid'})


        return Response(UserInformationSerializer(request.user).data)
    


# Dashboard
class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = UserInformationSerializer(request.user).data
        return Response(user)




# update profile
class UpdateUSerProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


    def partial_update(self, request, *args, **kwargs):
        if request.data.get("password") == request.data.get("password2") and  request.data.get('password') is not None:
            request.user.set_password(request.data.get("password"))
            request.user.save()
        elif request.data.get('password') != request.data.get('password2'):
            return Response({'error': 'Passwords  is invalid'})


        return super().partial_update(request, *args, **kwargs)


# Sing Up
class SingUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInformationSerializer



# set password
class UpdatePassword(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("password") == request.data.get("password2") and request.data.get('password') is not None:
            request.user.set_password(request.data.get("password"))
            request.user.save()
        elif request.data.get('password') != request.data.get('password2'):
            return Response({'error': 'Passwords  is invalid'})


        return Response(UserInformationSerializer(request.user).data)
