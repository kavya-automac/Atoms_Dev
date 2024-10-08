# Generated by Django 5.0.1 on 2024-01-20 07:52

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Card_Type', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Users_Schema"."CardInventory',
            },
        ),
        migrations.CreateModel(
            name='Layers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Layer_Type', models.CharField(max_length=200)),
                ('Layer_Name', models.CharField(max_length=200)),
                ('Company_Logo', models.URLField(blank=True, null=True)),
                ('Location', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'Users_Schema"."Layers',
            },
        ),
        migrations.CreateModel(
            name='MachineDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Machine_id', models.CharField(max_length=300)),
                ('Machine_Name', models.CharField(max_length=300)),
                ('Model_No', models.CharField(max_length=300)),
                ('Gateway_Id', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'Users_Schema"."MachineDetails',
            },
        ),
        migrations.CreateModel(
            name='Manuals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Filename', models.CharField(blank=True, max_length=300, null=True)),
                ('FileUrl', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Users_Schema"."Manuals',
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Module_Name', models.CharField(max_length=200)),
                ('icons', models.URLField(blank=True, null=True)),
                ('Type', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Users_Schema"."Modules',
            },
        ),
        migrations.CreateModel(
            name='TechnicalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item_Name', models.CharField(max_length=300)),
                ('Manufacture_Name', models.CharField(max_length=300)),
                ('Manufacture_Model_No', models.CharField(max_length=300)),
                ('Expiry_Date', models.DateField()),
            ],
            options={
                'db_table': 'Users_Schema"."TechnicalDetails',
            },
        ),
        migrations.CreateModel(
            name='IOList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IO_type', models.CharField(max_length=100)),
                ('IO_name', models.CharField(max_length=100)),
                ('IO_value', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None)),
                ('IO_color', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None)),
                ('IO_Range', models.CharField(blank=True, max_length=100)),
                ('IO_Unit', models.CharField(blank=True, max_length=100)),
                ('Control', models.BooleanField(default=False)),
                ('machine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Atoms_users.machinedetails')),
            ],
            options={
                'db_table': 'Users_Schema"."IO_List',
            },
        ),
        migrations.AddField(
            model_name='machinedetails',
            name='Manuals',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Atoms_users.manuals'),
        ),
        migrations.AddField(
            model_name='machinedetails',
            name='Technical_Details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Atoms_users.technicaldetails'),
        ),
    ]
