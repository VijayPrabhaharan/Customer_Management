# Generated by Django 4.1 on 2022-10-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='profile_pic1', null=True, upload_to=''),
        ),
    ]
