from rest_framework import serializers
from .models import Order, OrderData, OrderHistory, OrderProducts, City, State
import datetime
from main.serializers import ProductVariantSerializer


# order products serializer
class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = OrderProducts
        exclude = ['order']


# order data serializer
class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        exclude = ['order']


# state serializer
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


# city serializer
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


# order serializer
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True, read_only=True)
    data = OrderDataSerializer(read_only=True)
    state = StateSerializer()
    city = CitySerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only = ['date']


    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        OrderHistory.objects.create(order=order, status=order.status, comment='Order created by {}'.format(order.get_full_name()))

        return order


    def update(self, instance, validate_data):
        status = validate_data.get('status', instance.status)
        
        if instance.status != status:
            OrderHistory.objects.create(order=instance, status=status, comment='Order status is updated')

        instance.status = status
        
        return instance



