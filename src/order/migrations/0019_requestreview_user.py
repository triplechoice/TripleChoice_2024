# Generated by Django 4.0 on 2021-12-20 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_delete_userrole'),
        ('order', '0018_alter_requestreview_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestreview',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
        ),
    ]
