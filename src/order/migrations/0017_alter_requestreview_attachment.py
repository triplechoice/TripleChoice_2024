# Generated by Django 4.0 on 2021-12-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_rename_order_id_requestreview_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestreview',
            name='attachment',
            field=models.FileField(help_text='PDF file ', upload_to=''),
        ),
    ]
