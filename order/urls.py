from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.OrderCreateView.as_view()),
    path('orders/<int:pk>', views.OrderCreateView.as_view()),
    path('payments', views.PaymentTypeView.as_view()),
]
