from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path("login/verify/", TokenVerifyView.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('check_number', views.CheckNubmer.as_view()),
    path("send_sms", views.SendSms.as_view()),
    path("sing-up", views.SingUpView.as_view()),
    path('code_validate', views.CodeValidate.as_view()),
    path("update_profile", views.UpdateUSerProfileView.as_view()),
    path("update_password", views.UpdatePassword.as_view()),
    path('reset_password', views.ResetPassword.as_view())
]