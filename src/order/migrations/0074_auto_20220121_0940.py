# Generated by Django 3.2.9 on 2022-01-21 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0073_merge_20220121_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='refund_info',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderinfohistory',
            name='refund_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
