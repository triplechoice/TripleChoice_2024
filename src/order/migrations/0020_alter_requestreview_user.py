# Generated by Django 4.0 on 2021-12-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_delete_userrole'),
        ('order', '0019_requestreview_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
        ),
    ]
