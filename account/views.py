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
import string, random
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
#from twilio.rest import Client

# generate password
def generate_pass():
    password = ''

    pass_len = random.randint(8, 20)
    alf_count = random.randint(pass_len//4, pass_len//2)
    nbm_count = pass_len - alf_count

    alf = string.ascii_uppercase
    nbm = string.digits

    for _ in range(alf_count):
        password += random.choice(alf)

    for _ in range(nbm_count):
        password += random.choice(nbm)

    password = list(password)
    random.shuffle(password)

    return ''.join(password)

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
        }, 60)
        cache.set(f'counter_{nbm}', 0, 60)


        print(nbm, code)

        return Response(cache.get(nbm))


# check code
class CodeValidate(views.APIView):
    def post(self, request, format=None):
        nbm = request.data.get("nbm")

        if cache.get(f'counter_{nbm}', 5) >= 5:
            cache.delete_many([nbm, f'counter_{nbm}'])
        
        my_cache = cache.get(nbm, {})
        try:
            cache.incr(f'counter_{nbm}', 1)
        except:
            pass

        code = request.data.get("code")
        in_cache_code = my_cache.get('code')


        if code is None or  in_cache_code is None:
            return Response({'error': 'Code is invalid'}, status=status.HTTP_403_FORBIDDEN)


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
class ResetPassword(views.APIView):
    def post(self, request, format=None):
        nbm = request.POST.get('nbm')
        user = get_object_or_404(User.objects.filter(is_active=True), nbm=nbm)

        password = generate_pass()
        print(password)
        user.set_password(password)
        user.save()

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


    def perform_create(self, serializer):
        password = generate_pass()
        serializer.validated_data['password'] = password
        print(password)
        user = serializer.save()
        cache.set(serializer.validated_data.get('nbm'), password)

        return user


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



# new password
class NewPassword(views.APIView):
    def post(self, request, format=None):
        password = generate_pass()
        nbm = request.data.get("nbm")

        try: 
            user = User.objects.get(nbm=nbm)
        except:
            return Response({'error': 'nbm is incorrect'})

        user.set_password(password)
        user.save()
        print(password)

        serializer = UserInformationSerializer(user)

        return Response(serializer.data)



# log out
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #try:
        refresh_token = request.data["refresh_token"]
        access_tonen = request.data['access_token']
        token = RefreshToken(refresh_token)
        access = AccessToken(access_tonen)
        access.blacklist()
        token.blacklist()

        return Response({'success': True}, status=status.HTTP_205_RESET_CONTENT)
        #except:
        #    return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


