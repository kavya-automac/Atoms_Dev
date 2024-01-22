from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Layers(models.Model):  # for companies,partnerships,customers ,plant and lines
    objects = models.Manager()
    Layer_Type = models.CharField(max_length=200)
    Layer_Name = models.CharField(max_length=200)
    Company_Logo = models.URLField(blank=True,null=True)
    Location = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."Layers'

    def __str__(self):
        return self.Layer_Name


class Modules(models.Model):  #  page names
    Module_Name = models.CharField(max_length=200)  # page name
    icons = models.URLField(blank=True, null=True)
    Type = models.CharField(max_length=200)  # page or subpage

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."Modules'

    def __str__(self):
        return self.Module_Name


class CardInventory(models.Model): # total number of cards line or bar or text ...
    Card_Type = models.CharField(max_length=200)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."CardInventory'

    def __str__(self):
        return self.Card_Type

class Manuals(models.Model):
    Filename = models.CharField(max_length=300,blank=True,null=True)
    FileUrl = models.URLField(blank=True,null=True)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."Manuals'

    def __str__(self):
        return self.Filename


class TechnicalDetails(models.Model):
    Item_Name = models.CharField(max_length=300)
    Manufacture_Name = models.CharField(max_length=300)
    Manufacture_Model_No = models.CharField(max_length=300)
    Expiry_Date = models.DateField()

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."TechnicalDetails'

    def __str__(self):
        return self.Item_Name


class MachineDetails(models.Model):
    Machine_id = models.CharField(max_length=300)
    Machine_Name = models.CharField(max_length=300)
    Model_No = models.CharField(max_length=300)
    Gateway_Id = models.CharField(max_length=300)
    Manuals = models.ManyToManyField(Manuals,blank=True)
    Technical_Details = models.ManyToManyField(TechnicalDetails,blank=True)
    IO_Group_Id = models.CharField(max_length=300,blank=True)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."MachineDetails'

    def __str__(self):
        return "%s %s" %(self.Machine_id,self.Machine_Name)


class IOList(models.Model):
    IO_Group=models.CharField(max_length=300)
    IO_type=models.CharField(max_length=100)
    IO_name=models.CharField(max_length=100)
    IO_value=ArrayField(models.CharField(max_length=100,blank=True))
    IO_color=ArrayField(models.CharField(max_length=100,blank=True))
    IO_Range=models.CharField(max_length=100,blank=True)
    IO_Unit=models.CharField(max_length=100,blank=True)
    Control=models.BooleanField(default=False)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."IO_List'

    def __str__(self):
        return str(self.IO_Group)


class Nested_Table(models.Model):
    Node_Id = models.IntegerField()
    Node_Left=models.IntegerField()
    Node_Right=models.IntegerField()
    Property = models.CharField(max_length=200)

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."Nested_Table'

    def __str__(self):
        return "%s %s %s %s" % (str(self.Node_Id),str(self.Node_Left),str(self.Node_Right),self.Property)



class User_details(models.Model):
    objects = models.Manager()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to='images', blank=True)
    Mobile_No = models.CharField(max_length=12, blank=True)
    Company_id = models.ForeignKey(Layers, null=True, blank=True, on_delete=models.CASCADE)



    def __str__(self):
        return self.user_id.username


class MachineCardsList(models.Model):  # datapoints for particular kpi
    Machine_Id = models.ManyToManyField(MachineDetails,blank=True)
    Kpi_Name = ArrayField(models.CharField(max_length=200, blank=True))
    DataPoints = ArrayField(models.CharField(max_length=200, blank=True))
    mode = models.CharField(max_length=100,blank=True)
    Conversion_Fun = models.CharField(max_length=100,blank=True)
    X_Label = models.CharField(max_length=100,blank=True)
    Y_Label = models.CharField(max_length=100,blank=True)
    Ledger = ArrayField(models.CharField(max_length=200, blank=True))

    class Meta:
        app_label = 'Atoms_users'
        db_table = 'Users_Schema"."MachineCardsList'

    def __str__(self):
        return str(self.Kpi_Name)






