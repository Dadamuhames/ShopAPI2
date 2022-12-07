from django.contrib import admin
from .models import Order, OrderData, OrderHistory, OrderProducts, State, City, PaymentTyps, Promocode
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderHistory)
admin.site.register(OrderProducts)
admin.site.register(OrderData)
admin.site.register(State)
admin.site.register(City)
admin.site.register(PaymentTyps)
admin.site.register(Promocode)

