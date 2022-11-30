from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path("login/varify/", TokenVerifyView.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('check_number', views.CheckNubmer.as_view()),
    path("sing-up", views.SingUpView.as_view())
]