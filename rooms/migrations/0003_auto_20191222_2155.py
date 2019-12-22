# Generated by Django 2.2.5 on 2019-12-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20191222_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='houserule',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
