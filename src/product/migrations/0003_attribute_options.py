# Generated by Django 3.2.9 on 2021-11-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20211122_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='options',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
