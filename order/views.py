from django.shortcuts import render
from rest_framework import views, viewsets, generics, status, mixins, permissions
from .serializers import OrderSerializer, PaymentTypeSerializer, StateSerializer, CitySerializer, OrdersDetailSerializer, OrderAplicationSerializer
from main.serializers import CartViewSerializer
from rest_framework.response import Response
from .models import Order, OrderData, OrderHistory, OrderProducts, PaymentTyps, State, City, OrderAplication
from rest_framework.permissions import IsAuthenticated
from main.models import ProductVariants
from .filters import OrderFilter
from django_filters import rest_framework as filter
from rest_framework.pagination import PageNumberPagination
# Create your views here.


# paginators
class BasePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


# orders list
class MyOrders(generics.ListAPIView):
    serializer_class = OrdersDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = BasePagination

    def get_queryset(self):
        orders = Order.objects.filter(
            user=self.request.user).exclude(status='Отменено')
        if self.request.GET.get('status') is not None and self.request.GET.get('status') != 'Отменено':
            status = self.request.GET.get('status')
            orders = Order.objects.filter(status=status)

        return orders

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# create order
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = BasePagination
    

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
        print(lst)
        total = 0
        for it in lst:
            print(it)
            product = ProductVariants.objects.get(id=int(it['id']))
            price = product.price * int(it['count'])
            total += price

            OrderProducts.objects.create(
                order = order,
                product = product,
                price = price,
                qty = int(it['count'])
            )

        order.price = total
        order.save()



        ip = self.request.META.get('REMOTE_ADDR')
        agent = self.request.META.get('HTTP_USER_AGENT')
        lng = self.request.META.get("HTTP_ACCEPT_LANGUAGE")

        OrderData.objects.create(order=order, ip=ip, user_agent=agent, lng=lng)

        return Response(order)



# payment type view
class PaymentTypeView(generics.ListAPIView):
    queryset = PaymentTyps.objects.filter(parent=None)
    serializer_class = PaymentTypeSerializer


# get states
class StatesView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer


# get cities
class CityView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    

# create aplication 
class AplicationCreateView(generics.CreateAPIView):
    queryset = OrderAplication.objects.all()
    serializer_class = OrderAplicationSerializer





