# Generated by Django 4.2.4 on 2023-09-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0003_alter_orders_description_alter_orders_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='operator',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('1', 'Yangi'), ('2', 'Qabul qilind'), ('3', 'Yetkazilmoqda'), ('4', 'Yetqazib berildi'), ('5', 'Qaytib kelgan'), ('6', 'Keyin Oladi'), ('7', 'Qayta Qongiroq'), ('8', 'Arxiv'), ('9', 'Dubl'), ('10', 'Ban')], default=1, max_length=100),
        ),
    ]
