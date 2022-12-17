from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.OrderCreateView.as_view()),
    path('my_orders', views.MyOrders.as_view()),
    path('payments', views.PaymentTypeView.as_view()),
    path('get_cities', views.CityView.as_view()),
    path("get_states", views.StatesView.as_view())
]
