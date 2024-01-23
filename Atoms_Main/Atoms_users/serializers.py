from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(error_messages={
        'blank': ' password_field_cannot_be_blank.'
    })

    username = serializers.CharField(error_messages={
        'blank': 'username_field_cannot_be_blank.'
    })



    class Meta:
            model = User
            fields = ('username', 'password')


class user_details_serializer_all (serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = '__all__'