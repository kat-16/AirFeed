# Generated by Django 2.0.7 on 2018-08-20 06:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fil_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='idf',
            field=models.CharField(default=uuid.UUID('dfe01388-2154-4bb9-a49f-b7382bf87007'), max_length=64, verbose_name='Identification key'),
        ),
    ]
