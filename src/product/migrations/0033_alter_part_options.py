# Generated by Django 3.2.9 on 2022-10-18 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_merge_20220105_0934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ('title',)},
        ),
    ]
