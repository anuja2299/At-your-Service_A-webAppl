# Generated by Django 4.0.5 on 2022-06-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atYourService', '0006_rename_date_joined_client_datejoined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='Name',
            field=models.CharField(default='', max_length=100),
        ),
    ]