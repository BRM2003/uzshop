# Generated by Django 4.2.4 on 2023-09-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_goods_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='price_for_admin',
            field=models.IntegerField(default=0),
        ),
    ]
