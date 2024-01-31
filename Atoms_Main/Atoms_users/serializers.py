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
        fields =[ "node_id","Machine_Name","Machine_id","Model_No"]

class layerSerializer(serializers.ModelSerializer):#dropdown
    class Meta:
        model = Layers
        fields = ["Layer_Name","Layer_Type"]


class ManualsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuals
        fields = ['Filename','FileUrl']

class TechnicalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDetails
        fields = ['Item_Name','Manufacture_Name','Manufacture_Model_No','Expiry_Date']




class Details_serializer(serializers.ModelSerializer):#details mauals and techinedetails
    Manuals = ManualsSerializer(many=True, read_only=True)
    Technical_Details = TechnicalDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = MachineDetails
        fields = '__all__'



class only_details_serailizers(serializers.ModelSerializer):
    class Meta:
        model = MachineDetails
        fields = ['Machine_Name','Model_No','Gateway_Id']


class IO_list_serializer(serializers.ModelSerializer): #iostatus api for keys # trail_details # kpis for keys
    class Meta:
        model=IOList
        # fields = '__all__'
        fields = ('IO_type','IO_name','IO_value','IO_color','IO_Unit','Control')

