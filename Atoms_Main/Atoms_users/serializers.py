from . models import *
from rest_framework import serializers

class layerSerializer(serializers.ModelSerializer):#dropdown
    class Meta:
        model = Layers
        fields = ["Layer_Name","Layer_Type"]

