# Generated by Django 4.2.4 on 2023-09-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterField(
            model_name='orders',
            name='region',
            field=models.TextField(default='uz', max_length=32),
        ),
    ]
