from rest_framework import serializers
from .models import User, telephone_validator

# login serializer
class LoginSerializer(serializers.Serializer):
    nbm = serializers.CharField(validators=[telephone_validator])
    password = serializers.CharField()


# user serializer
class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'last_name', 'nbm', 'email', 'state', 'city', 'post_ind', 'adres', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user





