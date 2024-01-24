from django import forms
from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin



@admin.register(IOList)
class IOList_Admin(admin.ModelAdmin):
    list_display = ['id','IO_Group','IO_type','IO_name','IO_value','IO_color','IO_Range','IO_Unit','Control']


@admin.register(Nested_Table)
class Nested_Table_Admin(admin.ModelAdmin):
    list_display = ['id','Node_Id','Node_Left','Node_Right','Property']
    search_fields = Nested_Table.SearchableFields


@admin.register(Layers)
class Layers_Admin(admin.ModelAdmin):
    list_display = ['id','Layer_Type','Layer_Name','Company_Logo','Location']


@admin.register(Modules)
class Modules_Admin(admin.ModelAdmin):
    list_display = ['id','Module_Name','icons','Type']


@admin.register(CardInventory)
class CardInventory_Admin(admin.ModelAdmin):
    list_display = ['id','Card_Type']


@admin.register(Manuals)
class Manuals_Admin(admin.ModelAdmin):
    list_display = ['id','Filename','FileUrl']


@admin.register(TechnicalDetails)
class TechnicalDetails_Admin(admin.ModelAdmin):
    list_display = ['id','Item_Name','Manufacture_Name','Manufacture_Model_No','Expiry_Date']

@admin.register(MachineDetails)
class MachineDetails_Admin(admin.ModelAdmin):
    list_display = ['id','Machine_id','Machine_Name','Model_No','Gateway_Id','IO_Group_Id']
    # list_filter = ('IO_Group_Id',)




@admin.register(MachineCardsList)
class MachineCardsList_Admin(admin.ModelAdmin):
    list_display = ['id','Kpi_Name','DataPoints','mode','Conversion_Fun','X_Label','Y_Label','Ledger']





class UserDetailsInline(admin.StackedInline):
    model = User_details
    can_delete = False

class UserDetailsAdmin(AuthUserAdmin):
    list_display =['id','username']
    def add_view(self,*args,**kwargs):#for error
        self.inlines=[]
        return super(UserDetailsAdmin, self).add_view(*args, **kwargs)

    def change_view(self,*args,**kwargs):
        self.inlines =[UserDetailsInline]
        return super(UserDetailsAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User,UserDetailsAdmin)
admin.site.register(User_details)

