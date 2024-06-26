# Generated by Django 5.0.1 on 2024-01-20 11:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Atoms_users', '0006_alter_machinedetails_manuals_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineCardsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kpi_Name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None)),
                ('DataPoints', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None)),
                ('mode', models.CharField(blank=True, max_length=100)),
                ('Conversion_Fun', models.CharField(blank=True, max_length=100)),
                ('X_Label', models.CharField(blank=True, max_length=100)),
                ('Y_Label', models.CharField(blank=True, max_length=100)),
                ('Ledger', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None)),
                ('Machine_Id', models.ManyToManyField(blank=True, to='Atoms_users.machinedetails')),
            ],
            options={
                'db_table': 'Users_Schema"."MachineCardsList',
            },
        ),
    ]
