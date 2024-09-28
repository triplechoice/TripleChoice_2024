# Generated by Django 3.2.10 on 2022-01-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0066_auto_20220119_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestreview',
            name='supplier_cost_unit',
            field=models.CharField(choices=[('EUR', '€-EUR'), ('USD', '$-USD'), ('CNY', '¥-CNY')], default='USD', max_length=10),
        ),
    ]
