from django.contrib import admin

# Register your models here.
from . models import  *

@admin.register(MachineRawData)
class MachineRawData_Admin(admin.ModelAdmin):
    list_display = ['id','Db_Timestamp','Timestamp','Machine_Id','Machine_Location','Digital_Input','Digital_Output','Analog_Input','Analog_Output','Other']
    search_fields =MachineRawData.SearchableFields



@admin.register(CardsRawData)
class CardsRawData_Admin(admin.ModelAdmin):
    list_display = ['id','Timestamp','Machine_Id','Name','Value','Title','Mode']
    search_fields =CardsRawData.SearchableFields
