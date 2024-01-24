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


class user_details_serializer_all (serializers.ModelSerializer):#[login api, ]
    class Meta:
        model = User_details
        fields = '__all__'


class machine_details_serializer_machine_id_machine_name (serializers.ModelSerializer):#[machine_list api, ]
    node_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = MachineDetails
        fields =[ "node_id","Machine_Name","Model_No"]