from django.shortcuts import render
from rest_framework import views, viewsets, generics, status, mixins
from .serializers import OrderSerializer, PaymentTypeSerializer
from main.serializers import CartViewSerializer
from rest_framework.response import Response
from .models import Order, OrderData, OrderHistory, OrderProducts, PaymentTyps
from rest_framework.permissions import IsAuthenticated
from main.models import ProductVariants
# Create your views here.


class OrderCreateView(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    permission_classes = []
    

    def get_queryset(self):
        if self.request.user.is_authenticated:
            orders = Order.objects.filter(user=self.request.user).exclude(status='Canseled')
        else:
            if not self.request.session.session_key:
                self.request.session.cycle_key()
            sk = self.request.session.session_key
            orders = Order.objects.filter(session=sk)

        return orders
    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        order = serializer.save()
        
        if self.request.user.is_authenticated:
            order.user = self.request.user
        else:
            if not self.request.session.session_key:
                self.request.session.cycle_key()
            sk = self.request.session.session_key
            order.session = sk
        order.save()

        # may be another name
        # get products part
        lst = self.request.data.get('products')

        for it in lst:
            pass

            product = ProductVariants.objects.get(id=int(it['id']))
            price = product.price * int(it['count'])

            OrderProducts.objects.create(
                order = order,
                product = product,
                price = price,
                qty = int(it['count'])
            )



        ip = self.request.META.get('REMOTE_ADDR')
        agent = self.request.META.get('HTTP_USER_AGENT')
        lng = self.request.META.get("HTTP_ACCEPT_LANGUAGE")

        OrderData.objects.create(order=order, ip=ip, user_agent=agent, lng=lng)

        return Response(order)



# payment type view
class PaymentTypeView(generics.ListAPIView):
    queryset = PaymentTyps.objects.filter(parent=None)
    serializer_class = PaymentTypeSerializer


# payment order detail view
#class OrderDetailView(generics.RetrieveAPIView):
    





