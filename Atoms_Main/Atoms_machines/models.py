from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class MachineRawData(models.Model):
    objects = models.Manager()
    Db_Timestamp = models.DateTimeField(auto_now_add=True)
    Timestamp = models.DateTimeField()
    Machine_Id = models.CharField(max_length=150)
    Machine_Location = models.CharField(max_length=250)
    Digital_Input = ArrayField(models.BooleanField())
    Digital_Output = ArrayField(models.BooleanField())
    Analog_Input = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    Analog_Output = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    Other = ArrayField(models.CharField(max_length=100, default=True))
    SearchableFields=["Db_Timestamp","Timestamp","Machine_Id","Machine_Location"]



    class Meta:
        app_label = 'Atoms_machines'
        db_table = 'Machines_Schema"."MachineRawData'

    def __str__(self):
        return "%s %s %s" % (self.Db_Timestamp,self.Timestamp,self.Machine_Id)


class CardsRawData(models.Model):
    Timestamp = models.DateTimeField()
    Machine_Id = ArrayField(models.CharField(max_length=200, default=True))
    Name = ArrayField(models.CharField(max_length=200, default=True))
    Value = ArrayField(models.CharField(max_length=200, default=True))
    Title=models.CharField(max_length=200, default="")
    Mode = models.CharField(max_length=200, default="")
    SearchableFields = ["Timestamp", "Machine_Id", "Title"]

    class Meta:
        app_label = 'Atoms_machines'
        db_table = 'Machines_Schema"."CardsRawData'

    def __str__(self):
        return "%s %s %s" % (self.Title, self.Timestamp, self.Machine_Id)
