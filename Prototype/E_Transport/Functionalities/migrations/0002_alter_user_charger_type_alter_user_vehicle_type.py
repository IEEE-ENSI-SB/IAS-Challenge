# Generated by Django 4.2.7 on 2023-11-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Functionalities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Charger_Type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='Vehicle_Type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
