from rest_framework import serializers
from .models import *


class machineValues_serializer(serializers.ModelSerializer):
    class Meta:
        model=MachineRawData
        # fields = "__all__"
        fields = ('Db_Timestamp','Timestamp','Machine_Id','Machine_Location',
                  'Digital_Input','Digital_Output','Analog_Input','Analog_Output','Other')
