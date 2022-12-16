from rest_framework import serializers
from .models import Order, OrderData, OrderHistory, OrderProducts, City, State, Promocode, PaymentTyps
import datetime
from main.serializers import ProductVariantSerializer
from main.serializers import ReqursiveCategorySerializer


# order products serializer
class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer(read_only=True)

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


# order history serializer
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'


# payment typs serializer
class PaymentTypeSerializer(serializers.ModelSerializer):
    children = ReqursiveCategorySerializer(many=True)

    class Meta:
        model = PaymentTyps
        fields = '__all__'


# order serializer
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True, read_only=True)
    data = OrderDataSerializer(many=True, read_only=True)
    #state = StateSerializer(read_only=True)
    #city = CitySerializer(read_only=True)
    history = HistorySerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date', 'products', 'update_date']



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


#        code = validated_data.get('code')
#         if code is not None:
#           try:
#               promocode = Promocode.objects.get(code=code)
#               validated_data['promocode'] = promocode.id
#           except:
#               pass
#       name = validated_data.get('name')
